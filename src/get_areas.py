import sys
import mysql.connector
import gpxpy
import gpxpy.gpx

class areas:
	#DB_connection + query
	db = mysql.connector.connect(
	  host="cidco.ca",
	  user="crabnet",
	  password="crabnet213141$",
	  database="crabnet"
	)

	
	def __init__(self,query):
		self.query = query
		
	
	def get_data(self):
		cursor = areas.db.cursor()
		cursor.execute(self.query)
		result = cursor.fetchall()
		return result

test = areas("SELECT * FROM crabnet.dfo_engins WHERE type='CASIER/CAGE - TRAP/POT'")
data = test.get_data()
print(data)
