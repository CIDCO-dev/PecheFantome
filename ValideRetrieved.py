"""
# Copyright 2019 © Centre Interdisciplinaire de développement en Cartographie des Océans (CIDCO), Tous droits réservés

@Dominic_Gonthier

"""
import xlrd
import mysql.connector
import pandas as pd
from datetime import datetime
import re

"""Script pour importer  - 2020-07-15 - DFO-Lost-Gear - dans dfo_engins_recuperes"""

db = mysql.connector.connect(
  host="cidco.ca",
  user="crabnet",
  password="crabnet213141$",
  database="crabnet"
)


# Choix du fichier excel et de l'onglet
file_name="D:\CIDCO\dfo_engins_recuperes\\2020-07-15 - DFO-Lost-Gear.xlsx"
#sheet="RETRIEVED - 2019-2020"

wb=xlrd.open_workbook(file_name)
sheet=wb.sheet_by_index(1)
#data = pd.read_excel(io=file_name, sheet_name=sheet, skiprows=0)

# Get le curseur de la BD
cursor = db.cursor()

table= """
CREATE TABLE IF NOT EXISTS `dfo_engins_recuperes` (
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
query = "INSERT INTO dfo_engins_recuperes (retrieved, type, quantity, net_length, rope_length, LATITUDE, LONGITUDE, position) VALUES (%s, %s, %s, %s, %s, %s, %s, point(%s,%s))"


# Create a For loop to iterate through each row in the XLS file
#sheet.nrows

for r in range(1,sheet.nrows):
    try:
        try:
            try:
                date = re.search("\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$", sheet.cell(r, 0).value)
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
        quantity		= sheet.cell(r,4).value
        net_length		= sheet.cell(r,5).value
        rope_length	= sheet.cell(r,6).value

        try:
            latre= re.split("\D", sheet.cell(r,8).value)
            if latre[1] == "":
                continue
            else:
                d= int(latre[0])
                m=int(latre[1])
                try:
                    s = float((str(latre[2]) + '.' + (str(latre[3]))))

                except:
                    s=float(latre[2])
                LATITUDE = d + (m / 60) + (s / 3600)
        except:
            continue


        try:
            lonre= re.split("\D", sheet.cell(r,9).value)
            if lonre[1] == "":
                continue
            else:
                d2 = int(lonre[0])
                m2 = int(lonre[1])
                try:
                    s2=float((str(lonre[2]) + '.' + (str(lonre[3]))))
                    # s2 = float(lonre[2] + (lonre[3]))
                except:
                    s2 = float(lonre[2])
                LONGITUDE = 0-(d2 + (m2 / 60) + (s2 / 3600))
        except:
            continue

# 		# Assign values from each row
        values = (retrieved, type, quantity, net_length, rope_length, LATITUDE, LONGITUDE, LONGITUDE, LATITUDE)

# 		# Execute sql Query
        cursor.execute(query, values)
    except :
        print (r+1 , ' => ', (sheet.cell(r,0).value) , (sheet.cell(r,8).value) , (sheet.cell(r,9).value ))
        continue
# Close the cursor
cursor.close()

 # Commit the transaction
db.commit()
#
 # Close the database connection
db.close()
#

print ("Completed")