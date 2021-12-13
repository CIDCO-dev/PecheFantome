import GGlib
import mysql.connector
import gpxpy.gpx
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

#Ghost Gear databse
class GGDB:
	#default connexion
	def __init__(self,host="cidco.ca",user="crabnet",password="crabnet213141$",database="crabnet"):
		self.host = host
		self.user = user
		self.password = password
		self.databse = database
		self.cnnx = mysql.connector.connect(host = host,user = user,password = password, database = database)
		
	
	def query(self,query):
		# selection du type de query
		if query == "trap" :
			query = "SELECT * FROM crabnet.dfo_engins WHERE type='CASIER/CAGE - TRAP/POT'"
			cursor = self.cnnx.cursor() 
			cursor.execute(query) #executer query
			result = cursor.fetchall()
			return result
		else: #if query is not pre-made by CIDCO
			try: # try custom query
				cursor = cnnx.db.cursor()
				cursor.execute(query)
				result = cursor.fetchall()
				return result
			except mysql.connector.Error as err : #if query is not valid , print its error
				print(err)
	
	def toGPX(query_output, name, description):
		gpx = gpxpy.gpx.GPX()
		gpx.name = name
		gpx.description = description

		# Pour tous les casiers rapportes
		for trap in query_output:
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
		 
