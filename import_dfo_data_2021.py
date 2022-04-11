"""
# Copyright 2019 © Centre Interdisciplinaire de développement en Cartographie des Océans (CIDCO), Tous droits réservés

@Dominic_Gonthier

"""
import xlrd
import mysql.connector
import pandas as pd
from datetime import datetime
import re
import sys
import os

"""Script pour importer 2021 - Lost and Retrieved Gear Report - dans dfo_recuperes"""

def main_script(arg_host, arg_user, arg_password, arg_database, arg_filename):
  db = mysql.connector.connect(
    host=arg_host,
    user=arg_user,
    password=arg_password,
    database=arg_database
  )

  # Récupération du fichier excel 
  file_name=arg_filename


  wb=xlrd.open_workbook(file_name)
  sheet=wb.sheet_by_index(1)


  # Get le curseur de la BD
  cursor = db.cursor()

  table= """
  CREATE TABLE IF NOT EXISTS `dfo_recuperes` (
  `id` BIGINT(20)  NOT NULL   AUTO_INCREMENT PRIMARY KEY,
  `retrieved` DATETIME NOT NULL,
  `type` VARCHAR(255)  NOT NULL,
  `quantity` BIGINT(20)  NOT NULL,
  `net_length` BIGINT(20)  NOT NULL,
  `rope_length` BIGINT(20)  NOT NULL,
  `LATITUDE` DOUBLE  NOT NULL,
  `LONGITUDE` DOUBLE  NOT NULL,
  `position` GEOMETRY  NOT NULL     
  
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT ='';
  """
  cursor.execute(table)
  
  # Create the INSERT INTO sql query
  query = "INSERT INTO dfo_recuperes (retrieved, type, quantity, net_length, rope_length, LATITUDE, LONGITUDE, position) VALUES (%s, %s, %s, %s, %s, %s, %s, point(%s,%s))"
  
  
  # Create a For loop to iterate through each row in the XLS file
  #sheet.nrows
  
  for r in range(1,sheet.nrows):
    try:
        try:
            try:
                date = re.search("\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$", sheet.cell(r, 1).value)
                if date != None:
                    retrieved = sheet.cell(r, 0).value
                # else:

                    # try:
                    #     dateNum= sheet.cell(r, 0).value
                    #     retrieved = datetime.date(*xlrd.xldate_as_tuple(dateNum, 0))
                    # except:
                    #     retrieved= None
                    #     # pass
            except:
                try:
                    dateNum = sheet.cell(r, 0).value
                    retrieved = (datetime(*xlrd.xldate_as_tuple(43626.0, 0)))

                except:
                    retrieved = None
                    continue

        except:
            continue


        type			= sheet.cell(r,3).value
        quantity		= sheet.cell(r,6).value
        net_length		= sheet.cell(r,7).value
        rope_length	= sheet.cell(r,8).value
        LATITUDE= float(sheet.cell(r,10).value)
        LONGITUDE = float(sheet.cell(r,11).value)

 		# Assign values from each row
        values = (retrieved, type, quantity, net_length, rope_length, LATITUDE, LONGITUDE, LONGITUDE, LATITUDE)

 		# Execute sql Query
        cursor.execute(query, values)
    except :
        print (r+1 , ' => ', (sheet.cell(r,0).value) , (sheet.cell(r,8).value) , (sheet.cell(r,9).value ))
        continue
  
  cursor.close() # Close the cursor
  db.commit() # Commit the transaction
  db.close()  # Close the database connection
  print ("Completed")
  
  
    
def loar_arg():  
  # Detect and load the arguments
  if sys.argv[1] == "-h":
    help()
  elif sys.argv[1] == "-help": 
    help()
  else:
    arg_host=sys.argv[1]
    arg_user=sys.argv[2]
    arg_password=sys.argv[3]
    arg_database=sys.argv[4]
    arg_filename=sys.argv[5]
    
    main_script(arg_host, arg_user, arg_password, arg_database, arg_filename)
  

def help():
  # Display Help
  os.system('cls')    #clear screen for windows
  os.system('clear')  #clear screen for linux and mac
  print("Help")
  print("")
  print("Syntax: python import_dfo_data_2021.py [options]")
  print("")
  print("Options:")
  print("")
  print("help or h          Print Help Page")
  print("[Host]             Hostname or IP of the Database Server")
  print("[User]             User name to access to the Database")
  print("[Password]         Password to access to the Database")
  print("[DB_name]          Name of the Database")
  print("[filename]         File name")
  print("")
  print("Command line exemple.")
  print("python3 import_dfo_data_2021.py -help")
  print("python3 import_dfo_data_2021.py server_hostname user_name user_pass database_name file_name")
  print("python3 import_dfo_data_2021.py 192.168.1.100 user_test pass1234 data_test file.xlsx")
  print("python3 import_dfo_data_2021.py test.com user_test pass1234 data_test file.xlsx")
  print("")
  print("")
  print("")
  
  

if len(sys.argv) == 6:
  loar_arg()
else:  
  help() # not the right amount of argument


