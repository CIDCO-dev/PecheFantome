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


def display_help_message():
  # Display Help
  os.system('cls')    #clear screen for windows
  os.system('clear')  #clear screen for linux and mac
  print("Help")
  print("")
  print("Syntax: python import_dfo_data.py [options]")
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
  print("python3 import_dfo_data.py -help")
  print("python3 import_dfo_data.py server_hostname user_name user_pass database_name file_name")
  print("python3 import_dfo_data.py 192.168.1.100 user_test pass1234 data_test file.xlsx")
  print("python3 import_dfo_data.py test.com user_test pass1234 data_test file.xlsx")
  print("")
  print("")
  print("")
  
  

if len(sys.argv) != 6:
  display_help_message() # not the right amount of argument
else: 
  # Load command line arguments  
  db_host=sys.argv[1]
  db_user=sys.argv[2]
  db_password=sys.argv[3]
  db_database_name=sys.argv[4]
  input_filename=sys.argv[5]

  # Open database connection
  db = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_database_name
  )

  #Récupération du fichier excel 
  wb=xlrd.open_workbook(input_filename)
  sheet=wb.sheet_by_index(1)
  #data = pd.read_excel(io=file_name, sheet_name=sheet, skiprows=0)

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
 
  # Regex pour format de coordonées
  DMS = "[0-9]{2}\°[0-9]{2}\'."
  DDM="[0-9]{2}[\s\°][0-9]{2}[\.\,][0-9]{1,4}"

  # Create a For loop to iterate through each row in the XLS file
  #sheet.nrows

  for r in range(1,sheet.nrows):
    try:
        try:
            try:
                date = re.search("\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$", sheet.cell(r, 0).value)
                if date != None:
                    retrieved = sheet.cell(r, 0).value

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
        quantity		= sheet.cell(r,4).value
        net_length		= sheet.cell(r,5).value
        rope_length	= sheet.cell(r,6).value

        try:
            LATITUDE = None
            LONGITUDE= None
            if re.match(DMS, sheet.cell(r,8).value) !=None:    #   DMS to DD => DD = d + (min/60) + (sec/3600)
                #---------- Latitude ---------- DMS
                latre= re.split("\D", sheet.cell(r,8).value)
                d= int(latre[0])
                m=int(latre[1])
                try:
                    s = float((str(latre[2]) + '.' + (str(latre[3]))))
                except:
                    s=float(latre[2])
                LATITUDE = d + (m / 60) + (s / 3600)

                #---------- Longitude ---------- DMS

                lonre = re.split("\D", sheet.cell(r, 9).value)

                d2 = int(lonre[0])
                m2 = int(lonre[1])
                try:
                    s2 = float((str(lonre[2]) + '.' + (str(lonre[3]))))

                except:
                    s2 = float(lonre[2])
                LONGITUDE = -(d2 + (m2 / 60) + (s2 / 3600))

            elif re.match(DDM, sheet.cell(r, 8).value): # DD = Degrees + Decimal minutes / 60
                # print(r + 1, ' => ')

                #---------- Latitude ----------  DDM

                latre = re.split("\D", sheet.cell(r, 8).value)
                # print("DDM :", sheet.cell(r, 8).value)
                Degrees_lat = int(latre[0])
                minute_lat = int(latre[1])
                decimal_lat = (latre[2])
                dec_min_lat= float((str(minute_lat)) +'.' + (str(decimal_lat)))
                LATITUDE = Degrees_lat + (dec_min_lat / 60)

                #---------- Longitude ---------- DDM

                lonre = re.split("\D", sheet.cell(r, 9).value)
                # print("DDM :", sheet.cell(r, 9).value)
                Degrees_long = int(lonre[0])
                minute_long = int(lonre[1])
                decimal_long = (lonre[2])
                dec_min_long = float((str(minute_long)) +'.' + (str(decimal_long)))
                LONGITUDE = -(Degrees_long + (dec_min_long / 60))
        except:
            continue
        values = (retrieved, type, quantity, net_length, rope_length, LATITUDE, LONGITUDE, LONGITUDE, LATITUDE)  # Assign values from each row
        cursor.execute(query, values)  # Execute sql Query
        # print(r + 1, ' => OK ',(sheet.cell(r,8).value) , (sheet.cell(r,9).value ))
    except :
        # print (r+1 , ' ERREUR => ', (sheet.cell(r,0).value) , (sheet.cell(r,8).value) , (sheet.cell(r,9).value ))
        continue
  
  cursor.close() # Close the cursor
  db.commit() # Commit the transaction
  db.close()  # Close the database connection
  print ("Completed")
