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
		if query == "trap" :
			query = "SELECT * FROM crabnet.dfo_engins WHERE type='CASIER/CAGE - TRAP/POT'"
			self.query = query
		else:
			print("error")
		
	
	def get_data(self):
		cursor = areas.db.cursor()
		cursor.execute(self.query)
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

test = areas("trap")
data = test.get_data()
print(data)
