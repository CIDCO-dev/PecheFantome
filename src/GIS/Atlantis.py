import GGlib
import mysql.connector
import gpxpy.gpx
from xml.etree import ElementTree as ET
#from osgeo import ogr
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

#Ghost Gear databse
class GGDB:
	#default connexion
	def __init__(self,host="cidco.ca",user="crabnet",password="crabnet213141$",database="Pat_test_DB",port = "3306"):
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
		# selection du type de query
		if query == "trap" :
			query = "SELECT * FROM crabnet.dfo_engins WHERE type='CASIER/CAGE - TRAP/POT'"
			cursor = self.cnnx.cursor() 
			cursor.execute(query) #executer query
			self.result = cursor.fetchall()
			return self.result
		else: #if query is not pre-made by CIDCO
			try: # try custom query
				cursor = cnnx.db.cursor()
				cursor.execute(query)
				self.result = cursor.fetchall()
				return self.result
			except mysql.connector.Error as err : #if query is not valid , print its error
				print(err)
	
	def toGPX(self, name, description):
		gpx = gpxpy.gpx.GPX()
		gpx.name = name
		gpx.description = description

		# Pour tous les casiers rapportes
		for trap in self.result:
			longitude = trap[6]
			latitude  = trap[7]
			waypoint = gpxpy.gpx.GPXWaypoint()
			waypoint.longitude = longitude
			waypoint.latitude  = latitude
			waypoint.name      = "Casier {}".format(trap[0])
			waypoint.description = trap[2]
			gpx.waypoints.append(waypoint)
		self.xmlResult = gpx.to_xml()
		return self.result
		
	def importSHP(self,shpFilePath):
		db = "MYSQL:"+self.database+","+"host="+self.host+","+"user="+self.user+","+"password="+self.password+","+"port="+self.port
		#ogr2ogr = "/usr/bin/ogr2ogr"
		export = subprocess.Popen(["ogr2ogr", "-f", "MYSQL", db, "-a_srs", "EPSG:4326", shpFilePath])
		if (export.wait() != 0):
			return False
		else:
			return True
