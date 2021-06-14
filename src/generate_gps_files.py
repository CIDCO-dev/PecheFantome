import sys
import mysql.connector
import gpxpy
import gpxpy.gpx

def insideExclusionZone(longitude,latitude):
	zones_exclusion = ()

	print("TODO: exclure")
	return False

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
def get_areas():
	db = mysql.connector.connect(
	  host="cidco.ca",
	  user="crabnet",
	  password="crabnet213141$",
	  database="crabnet"
	)


	sectors=( { "name":"Secteur 1","polygon":(),"traps":()},{"name":"Secteur 2","polygon":(),"traps":()} )

	cursor = db.cursor()

	cursor.execute("SELECT * FROM crabnet.dfo_engins WHERE type='CASIER/CAGE - TRAP/POT'")

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
	areas = gpx.to_xml()
	return areas

print(get_areas())

	# Prendre ceux qui sont en dehors des zones d'exclusion
#	if not insideExclusionZone(longitude,latitude):
#		for s in sectors:
#			print(s['name'])
#			print("{} {}".format(longitude,latitude))
