import xlrd
import mysql.connector
import datetime
import sys
import os

def main_script(arg_host, arg_user, arg_password, arg_database, arg_filename):
  """Script pour le matching de dfo_engins_recuperes"""

# valider le nom du serveur ou le ip

  db = mysql.connector.connect(
    host=arg_host,
    user=arg_user,
    password=arg_password,
    database=arg_database
  )

  cursor = db.cursor()

  # creation de la table si inexistante
  cursor.execute("""
  create table IF NOT EXISTS dfo_after_match(
    `id` bigint(20) NOT NULL PRIMARY KEY ,
    `reported` datetime NOT NULL,
    `type` varchar(255) NOT NULL,
    `quantity` bigint(20) NOT NULL,
    `net_length` bigint(20) NOT NULL DEFAULT 0,
    `rope_length` bigint(20) NOT NULL DEFAULT 0,
    `LONGITUDE` double NOT NULL,
    `LATITUDE` double NOT NULL,
    `position` geometry NOT NULL,
    `id_r` bigint(20)    ,
    `retrieved_r` datetime  ,
    `type_r` varchar(255)  ,
    `quantity_r` bigint(20)  ,
    `net_length_r` bigint(20)  ,
    `rope_length_r` bigint(20)  ,
    `LATITUDE_r` double  ,
    `LONGITUDE_r` double ,
    `position_r` geometry ,
    `distance` double
  
    ) ENGINE=InnoDB AUTO_INCREMENT=7210 DEFAULT CHARSET=latin1
    ;
  """)

  # effacer les données deja presentes
  cursor.execute("TRUNCATE dfo_after_match;")

  # effectuer le match perdu/recupéré
  cursor.execute("""SELECT distinct *,
  ST_Distance_Sphere(t.position,c.position)
  from dfo_engins t
  left join 
  ( select * from dfo_engins_recuperes ) c
  on (ST_Distance_Sphere(t.position,c.position) <1000) 
  group by t.id
  order by t.id
  ;
  """)

  data= cursor.fetchall()



  restant_apres_match = {}

  for result in data:

    if result[9] == None:  # SI Aucun MATCH

        values = (result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7],  result[6], result[7], result[9], result[10], result[11], result[12], result[13], result[14], result[15], result[16],  result[16], result[15], result[18])
        # print("aucun match: ")
        # print("Perdu :    ", values[:8])
        # print("Recuperes :", values[10:])

    else:  # S'il y a un MATCH
        if result[9] not in restant_apres_match: # Engin recupéré encore jamais matché
            if result[12]<=result[3]:  # Qte recupérée < qte engin perdu
                qt_engin=result[3]-result[12]
                recupere_restant =0
                restant_apres_match.update({result[9]:recupere_restant})
                values = (result[0], result[1], result[2], qt_engin, result[4], result[5], result[6], result[7],  result[6], result[7], result[9], result[10], result[11], recupere_restant, result[13], result[14], result[15], result[16],  result[16], result[15], result[18])

                # print("first match: -------------------")
                # print("Perdu :    ", values[:9])
                # print("Recuperes :",values[9:])

            else:  # Qte recupérée > qte engin perdu
                qt_engin= 0
                recupere_restant=result[12]- result[3]
                restant_apres_match.update({result[9]: recupere_restant})
                values = (result[0], result[1], result[2], qt_engin, result[4], result[5], result[6], result[7],  result[6], result[7], result[9], result[10], result[11], recupere_restant, result[13], result[14], result[15], result[16],  result[16], result[15], result[18])

                # print("first match: Qte recuperes > qte perdu ")
                # print("Perdu :    ", values[:9])
                # print("Recuperes :",values[9:])

        else:  # Second Match pour engin récupéré
            if restant_apres_match.get(result[9]) == 0: # si qte restante associé a id_r deja a 0
                values = (result[0], result[1], result[2], qt_engin, result[4], result[5], result[6], result[7],  result[6], result[7], None, None, None, None, None, None, None, None,None,None,None)

                # print("AUTRE match: avec qte deja a 0 ")
                # print("Perdu :    ",values[:9])
                # print("Recuperes :",values[9:])


            else: # Second Match
                recupere_restant = restant_apres_match.get(result[9])
                if result[3]>=recupere_restant:
                    qt_engin = result[3] - recupere_restant
                    restant_apres_match.update({result[9]: 0})
                    values = (result[0], result[1], result[2], qt_engin, result[4], result[5], result[6], result[7],  result[6], result[7], result[9], result[10], result[11], 0, result[13], result[14], result[15], result[16],  result[16], result[15], result[18])

                    # print("Second match valide: -------------------")
                    # print("Perdu :    ",values[:9])
                    # print("Recuperes :",values[9:])


                else: # plus de recupéré que de perdu
                    qt_engin = 0
                    recupere_restant= recupere_restant-result[3]
                    restant_apres_match.update({result[9]: recupere_restant})
                    values = (result[0], result[1], result[2], qt_engin, result[4], result[5], result[6], result[7],  result[6], result[7], result[9], result[10], result[11], recupere_restant, result[13], result[14], result[15], result[16],  result[16], result[15], result[18])

                    # print("Second match valide: -----Reste encore des recupérés---")
                    # print("Perdu :    ",values[:9])
                    # print("Recuperes :",values[9:])

    cursor.execute("INSERT INTO dfo_after_match VALUES (%s,%s, %s, %s, %s, %s, %s, %s, point(%s,%s),%s,%s, %s, %s, %s, %s, %s, %s,point(%s,%s),%s);", values)

  # Close the cursor
  cursor.close()

  # Commit the transaction
  db.commit()
  #
  # Close the database connection
  db.close()
  #
  
def loar_arg():  
  if sys.argv[1] == "-h":
    help()
  elif sys.argv[1] == "-help": 
    help()
  else:
    arg_host=sys.argv[1]
    arg_user=sys.argv[2]
    arg_password=sys.argv[3]
    arg_database=sys.argv[4]
    
    main_script(arg_host, arg_user, arg_password, arg_database, arg_filename)
  

def help():
  # Display Help
  os.system('cls')    #clear screen for windows
  os.system('clear')  #clear screen for linux and mac
  print("Help")
  print("")
  print("Syntax: python appariement.py [options]")
  print("")
  print("Options:")
  print("")
  print("help or h          Print Help Page")
  print("[Host]             Hostname or IP of the Database Server")
  print("[User]             User name to access to the Database")
  print("[Password]         Password to access to the Database")
  print("[DB_name]          Name of the Database")
  print("")
  print("Command line exemple.")
  print("python3 appariement.py -help")
  print("python3 appariement.py server_hostname user_name user_pass database_name")
  print("python3 appariement.py 192.168.1.100 user_test pass1234 data_test")
  print("python3 appariement.py test.com user_test pass1234 data_test")
  print("")
  print("")
  print("")
  
  

if len(sys.argv) == 5:
  loar_arg()
else:  
  help() # not the right amount of argument


