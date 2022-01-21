import GGlib
import mysql.connector
import gpxpy.gpx
from xml.etree import ElementTree as ET
import subprocess

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

#Ghost Gear database
class GGDB:
	#default connexion
	def __init__(self,host="cidco.ca",user="crabnet",password="crabnet213141$",database="crabnet",port = "3306"):
		self.host = host
		self.user = user
		self.password = password
		self.database = database
		self.port = port
		self.cnnx = mysql.connector.connect(host = host,
                                            user = user,
                                            password = password, 
                                            database = database, 
                                            )
		
	
	def query(self,query):
		#premade querys
		if query == "trap" :
			query = "SELECT * FROM crabnet.dfo_engins WHERE type='CASIER/CAGE - TRAP/POT'"
			cursor = self.cnnx.cursor() 
			cursor.execute(query)
			self.result = cursor.fetchall()
			return self.result
		else: #if query is not pre-made by CIDCO
			try: # try custom query
				cursor = self.cnnx.cursor()
				cursor.execute(query)
				self.result = cursor.fetchall()
				return self.result
			except mysql.connector.Error as err : #if query is not valid , print its error
				print(err)
	
	def dfo_engins2GPX(self, name, description):
		gpx = gpxpy.gpx.GPX()
		gpx.name = name
		gpx.description = description

		# For all trap
		for trap in self.result:
			longitude = trap[6]
			latitude  = trap[7]
			waypoint = gpxpy.gpx.GPXWaypoint()
			waypoint.longitude = longitude
			waypoint.latitude  = latitude
			waypoint.name      = "Casier {}".format(trap[0])
			waypoint.description = trap[2]
			gpx.waypoints.append(waypoint)
		self.gpxResult = gpx.to_xml()
		return self.gpxResult
		
	def importSHP(self,shpFilePath):
		db = "MYSQL:"+self.database+","+"host="+self.host+","+"user="+self.user+","+"password="+self.password+","+"port="+self.port
		#ogr2ogr = "/usr/bin/ogr2ogr"
		export = subprocess.Popen(["ogr2ogr", "-f", "MYSQL", db, "-a_srs", "EPSG:4326", shpFilePath])
		if (export.wait() != 0):
			return False
		else:
			return True

	def extractSHP(self,table_name, polygon_name):
		try:
			query = "SELECT AsText(SHAPE) FROM "+table_name+" WHERE name ="+ polygon_name
			cursor = self.cnnx.cursor() 
			cursor.execute(query) #executer query
			result = cursor.fetchall()
			tupl = result[0]
			str_coord = tupl[0]
			if (str_coord.startswith("POLYGON")):
				str_coord = str_coord[9:-2]
				coordinates = str_coord.split(",")
				self.list_coordinates = []
				for pair in coordinates:
					pair = list(pair.split(" "))
					self.list_coordinates.append(pair)
			return self.list_coordinates
		except mysql.connector.Error as err : #if query is not valid , print its error
			print(err)
			
	
