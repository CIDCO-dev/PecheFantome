import sys
import mysql.connector
import gpxpy
import gpxpy.gpx

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
		else: #if query is not premade by the CIDCO
			self.query = query
			try: # try custom query
				cursor = query_DB.db.cursor()
				cursor.execute(self.query)
			except mysql.connector.Error as err : #if query is not valid , print error
				print(err)
		
	
	def get_areas(self):
		cursor = query_DB.db.cursor() #get object mysql-connector
		cursor.execute(self.query) #execute query
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
test = query_DB("tr")
data = test.get_areas()
print(data)
