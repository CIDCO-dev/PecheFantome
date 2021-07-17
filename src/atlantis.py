#import sys
import shapefile
import csv
import mysql.connector
import gpxpy
#import gpxpy.gpx # needed if installed via : apt install python3-gpxpy
from xml.etree import ElementTree as ET

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
def get_elements(element_name,element_description):
	db = mysql.connector.connect(
	  host="cidco.ca",
	  user="crabnet",
	  password="crabnet213141$",
	  database="crabnet"
	)
	cursor = db.cursor()
	cursor.execute("SELECT * FROM crabnet.dfo_engins WHERE type='CASIER/CAGE - TRAP/POT'")
	result = cursor.fetchall()

	gpx = gpxpy.gpx.GPX()
	gpx.name = element_name
	gpx.description = element_description

	# Pour tous les casiers rapportes
	for trap in result:
		longitude = trap[6]
		latitude  = trap[7]
		waypoint = gpxpy.gpx.GPXWaypoint()
		waypoint.longitude = longitude
		waypoint.latitude  = latitude
		waypoint.name      = "Casier {}".format(trap[0])
		waypoint.description = trap[2]
		gpx.waypoints.append(waypoint)
	areas = gpx.to_xml()
	return areas

def ecriture_points_2shp(liste_points, filename):
	w = shapefile.Writer(filename+".shp")
	w.field('name', 'C')
	w.multipoint(liste_points)
	w.record('multipoint')
	w.close()

def write_points_2csv(points_list, filename):
	with open(filename+".csv", 'w', newline='') as csvfile:
		file = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for coord in points_list:
			file.writerow(coord)

def extract_coordinates(areas):
	root = ET.fromstring(areas)
	liste_coordinates = []
	for i in range(1, len(root)):
		coord = root[i].attrib
		latitude = float(coord['lat'])
		longitude = float(coord['lon'])
		coordinate = [longitude, latitude]
		liste_coordinates += [coordinate]
	return liste_coordinates

def export_to(areas,export_format,filename):
	if export_format == "gpx":
		with open(filename+".gpx", "w") as f:
			f.write(areas)
	elif export_format == "shapefile":
		liste_coordinates = extract_coordinates(areas)
		ecriture_points_2shp(liste_coordinates,filename)
	elif export_format == "csv":
		liste_coordinates = extract_coordinates(areas)
		write_points_2csv(liste_coordinates,filename)
	else:
		error = "error: not a valid format ! \n options are : gpx, shapefile, csv"
		print(error)


