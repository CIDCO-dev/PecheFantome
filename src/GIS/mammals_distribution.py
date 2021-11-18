import os
import subprocess
import tqdm



def extract_contour(inputFilePath, outputPath):
	gdal_contour = "/usr/bin/gdal_contour"
	outputPath = inputFilePath[:-4]
	export = subprocess.Popen([gdal_contour, "-a", "sightings", "-i", "1", "-f", "ESRI Shapefile", inputFilePath, outputPath])
	export.wait()
	return True


"""
inputFilePath = "mammal/KD2.tif"
outputPath = "../"

status = extract_contour(inputFilePath,outputPath)
if(status == True):
	print("done")
"""

def export2DB():
	#ogr2ogr -f "MySQL"   MYSQL:"crabnet,host=localhost,user=admin,password=jmlespatate,port=3306" -a_srs "EPSG:4326" ‘/home/pat/PecheFantome/data/Zones Protegees MPO/DFO_MPA_MPO_ZPM.shp’
