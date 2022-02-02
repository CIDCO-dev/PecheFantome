import xlrd
import mysql.connector
import datetime

import re

"""Script pour le matching de dfo_engins_recuperes"""

db = mysql.connector.connect(
  host="cidco.ca",
  user="crabnet",
  password="crabnet213141$",
  database="crabnet"
)

cursor = db.cursor()

table= """
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
"""
truncate="TRUNCATE dfo_after_match;"

req="""SELECT distinct *,
ST_Distance_Sphere(t.position,c.position)
from dfo_engins t
left join 
( select * from dfo_engins_recuperes ) c
on (ST_Distance_Sphere(t.position,c.position) <1000) 
group by t.id
order by t.id
;
"""

query = """INSERT INTO dfo_after_match VALUES (%s,%s, %s, %s, %s, %s, %s, %s, point(%s,%s),%s,%s, %s, %s, %s, %s, %s, %s,point(%s,%s),%s);"""


# creation de la table si inexistante
cursor.execute(table)
# effacer les données deja presentes
cursor.execute(truncate)
# effectuer le match perdu/recupéré
cursor.execute(req)
data= cursor.fetchall()

j = {}

for r in data:

    if r[9] == None:  # SI Aucun MATCH

        values = (r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7],  r[6], r[7], r[9], r[10], r[11], r[12], r[13], r[14], r[15], r[16],  r[16], (r[15]), r[18])
        # print("aucun match: ")
        # print("Perdu :    ", values[:8])
        # print("Recuperes :", values[10:])

    else:  # S'il y a un MATCH
        if r[9] not in j: # Engin recupéré encore jamais matché
            if r[12]<=r[3]:  # Qte recupérée < qte engin perdu
                qt=r[3]-r[12]
                qtr=0
                j.update({r[9]:qtr})
                values = (r[0], r[1], r[2], qt, r[4], r[5], r[6], r[7],  r[6], r[7], r[9], r[10], r[11], qtr, r[13], r[14], r[15], r[16],  r[16], (r[15]), r[18])

                # print("first match: -------------------")
                # print("Perdu :    ", values[:9])
                # print("Recuperes :",values[9:])

            else:  # Qte recupérée > qte engin perdu
                qt= 0
                qtr=r[12]- r[3]
                j.update({r[9]: qtr})
                values = (r[0], r[1], r[2], qt, r[4], r[5], r[6], r[7],  r[6], r[7], r[9], r[10], r[11], qtr, r[13], r[14], r[15], r[16],  r[16], (r[15]), r[18])

                # print("first match: Qte recuperes > qte perdu ")
                # print("Perdu :    ", values[:9])
                # print("Recuperes :",values[9:])

        else:  # Second Match pour engin récupéré
            if j.get(r[9]) == 0: # si qte restante associé a id_r deja a 0
                values = (r[0], r[1], r[2], qt, r[4], r[5], r[6], r[7],  r[6], r[7], None, None, None, None, None, None, None, None,None,None,None)

                # print("AUTRE match: avec qte deja a 0 ")
                # print("Perdu :    ",values[:9])
                # print("Recuperes :",values[9:])


            else: # Second Match
                qtr = j.get(r[9])
                if r[3]>=qtr:
                    qt = r[3] - qtr
                    j.update({r[9]: 0})
                    values = (r[0], r[1], r[2], qt, r[4], r[5], r[6], r[7],  r[6], r[7], r[9], r[10], r[11], 0, r[13], r[14], r[15], r[16], r[16], (r[15]), r[18])

                    # print("Second match valide: -------------------")
                    # print("Perdu :    ",values[:9])
                    # print("Recuperes :",values[9:])


                else: # plus de recupéré que de perdu
                    qt = 0
                    qtr= qtr-r[3]
                    j.update({r[9]: qtr})
                    values = (r[0], r[1], r[2], qt, r[4], r[5], r[6], r[7], r[6], r[7], r[9], r[10], r[11], qtr, r[13], r[14], r[15], r[16], r[16], (r[15]), r[18])

                    # print("Second match valide: -----Reste encore des recupérés---")
                    # print("Perdu :    ",values[:9])
                    # print("Recuperes :",values[9:])

    cursor.execute(query, values)

# Close the cursor
cursor.close()

# Commit the transaction
db.commit()
#
# Close the database connection
db.close()
#

