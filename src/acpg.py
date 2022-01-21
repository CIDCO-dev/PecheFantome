import sys
import mysql.connector
import gpxpy
import csv

#############################################################
#      ******  *******       **     ******   ****     ** ******** **********
#     **////**/**////**     ****   /*////** /**/**   /**/**///// /////**///
#    **    // /**   /**    **//**  /*   /** /**//**  /**/**          /**
#   /**       /*******    **  //** /******  /** //** /**/*******     /**
#   /**       /**///**   **********/*//// **/**  //**/**/**////      /**
#   //**    **/**  //** /**//////**/*    /**/**   //****/**          /**
#    //****** /**   //**/**     /**/******* /**    //***/********    /**
#     //////  //     // //      // ///////  //      /// ////////     //
#
#
#         __       __
#        / <`     '> \
#       (  / @   @ \  )
#        \(_ _\_/_ _)/
#      (\ `-/     \-' /)
#       "===\     /==="
#        .==')___(`==.
#       ' .='     `=.
#
##############################################################
db = mysql.connector.connect(
  host="cidco.ca",
  user="crabnet",
  password="crabnet213141$",
  database="crabnet"
)



zonesCursor = db.cursor()

zonesCursor.execute("SELECT OGR_FID,name FROM crabnet.acpg")

zonesResults = zonesCursor.fetchall()

for retrievalZone in zonesResults:
	#Ex:
	#(1, 'Baie des chaleurs')
	#(2, 'Canal de Grande-Rivière')
	#(3, 'Nord Shediac Valley')
	#(4, 'Western Bradelle Valley')
	#(5, 'Eastern Bradelle Valley')
	print("Retrieving traps in {} (ID: {})".format(retrievalZone[1],retrievalZone[0]))

	trapsCursor = db.cursor()

	trapsCursor.execute("SELECT * FROM dfo_engins engins WHERE ST_Contains((SELECT SHAPE FROM acpg WHERE OGR_FID={}),Point(engins.LONGITUDE,engins.LATITUDE))".format(retrievalZone[0]))

	trapsResult = trapsCursor.fetchall()

	if len(trapsResult) > 0:
		gpx = gpxpy.gpx.GPX()
		gpx.name = retrievalZone[1]
		gpx.description = "Casiers de peche au crabe perdus dans la zone {}".format(retrievalZone[1])

		for trap in trapsResult:
			longitude = trap[6]
			latitude  = trap[7]

			waypoint = gpxpy.gpx.GPXWaypoint()
			waypoint.longitude = longitude
			waypoint.latitude  = latitude
			waypoint.symbol    = 'Marks-Mooring-Float'
			waypoint.name      = "Casier {}".format(trap[0])
			waypoint.description = trap[2]
			gpx.waypoints.append(waypoint)

		fileName = retrievalZone[1].replace(" ","")

		#Write GPX
		with open("{}.gpx".format(fileName),"w") as gpxFile:
			gpxFile.write(gpx.to_xml())

		#Write CSV
		with open('{}.csv'.format(fileName), 'w', newline='') as csvFile:
			csvwriter = csv.writer(csvFile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
			for trap in trapsResult:
				csvwriter.writerow([trap[6],trap[7]])

	trapsCursor.close()

zonesCursor.close()

#cursor = db.cursor()

#cursor.execute("SELECT * FROM crabnet.dfo_engins WHERE type='CASIER/CAGE - TRAP/POT'")

#result = cursor.fetchall()

#gpx = gpxpy.gpx.GPX()
#gpx.name = 'Casiers perdus'
#gpx.description = 'Casiers de peche au crabe perdus'

# Pour tous les casiers rapportes
#for trap in result:
#	longitude = trap[6]
#	latitude  = trap[7]

	# TODO: exclude, and see if in zone
#	waypoint = gpxpy.gpx.GPXWaypoint()
#	waypoint.longitude = longitude
#	waypoint.latitude  = latitude
#	#waypoint.symbol    = 'Marks-Mooring-Float'
#	waypoint.name      = "Casier {}".format(trap[0])
#	waypoint.description = trap[2]
#	gpx.waypoints.append(waypoint)


#print(gpx.to_xml())

	# Prendre ceux qui sont en dehors des zones d'exclusion
#	if not insideExclusionZone(longitude,latitude):
#		for s in sectors:
#			print(s['name'])
#			print("{} {}".format(longitude,latitude))
