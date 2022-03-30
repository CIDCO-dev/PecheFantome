import xlrd
import mysql.connector
import datetime
import sys

def main():
  """Script pour le matching de dfo_engins_recuperes"""

  db = mysql.connector.connect(
    host="cidco.ca",
    user="crabnet",
    password="crabnet213141$",
    database="crabnet"
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

def help():
    print("help")

if sys.argv == 1:
  help()
else:  
  print("argument détecté")

print(f"Arguments count: {len(sys.argv)}")
  for i, arg in enumerate(sys.argv):
    print(f"Argument {i:>6}: {arg}")
