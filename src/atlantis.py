import sys
import mysql.connector
import gpxpy
import gpxpy.gpx # needed if installed via : apt install python3-gpxpy

class query_DB:
	#DB_connection
	db = mysql.connector.connect(
	  host="cidco.ca",
	  user="crabnet",
	  password="crabnet213141$",
	  database="crabnet"
	)

	
	def __init__(self,query):
		# selection du type de query
		if query == "trap" :
			query = "SELECT * FROM crabnet.dfo_engins WHERE type='CASIER/CAGE - TRAP/POT'"
			self.query = query
		else: #Si la query n'est pas pre-fait par le CIDCO
			self.query = query
			try: # try custom query
				cursor = query_DB.db.cursor()
				cursor.execute(self.query)
			except mysql.connector.Error as err : #si la query n'est pas valide , print error
				print(err)
		
	#get areas de l'objet query_DB
	def get_areas(self):
		cursor = query_DB.db.cursor() 
		cursor.execute(self.query) #executer query
		result = cursor.fetchall()
		gpx = gpxpy.gpx.GPX()
		gpx.name = 'Casiers perdus'
		gpx.description = 'Casiers de peche au crabe perdus'

		# Pour tous les casiers rapportes
		for trap in result:
			longitude = trap[6]
			latitude  = trap[7]

			# TODO: exclude, and see if in zone
			waypoint = gpxpy.gpx.GPXWaypoint()
			waypoint.longitude = longitude
			waypoint.latitude  = latitude
			#waypoint.symbol    = 'Marks-Mooring-Float'
			waypoint.name      = "Casier {}".format(trap[0])
			waypoint.description = trap[2]
			gpx.waypoints.append(waypoint)
		result = gpx.to_xml()
			
		return result

#usage
test = query_DB("trap")
data = test.get_areas()
print(data)
