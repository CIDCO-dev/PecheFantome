import os
import subprocess
import tqdm



def extract_contour(inputFilePath, outputFilePath):
	gdal_contour = "/usr/bin/gdal_contour"
	if not os.path.exists(inputFilePath):
		print("input File Path does not exist")
		return false
	export = subprocess.Popen([gdal_contour, "-a", "sightings", "-i", "1", "-f", "ESRI Shapefile", inputFilePath, outputFilePath])
	export.wait()
	return True



inputFilePath = "mammal/KD2.tif"
outputPath = "../kd2.shp"

status = extract_contour(inputFilePath,outputPath)
if(status == True):
	print("done")


def export2DB():
	#ogr2ogr -f "MySQL"   MYSQL:"crabnet,host=localhost,user=admin,password=jmlespatate,port=3306" -a_srs "EPSG:4326" ‘/home/pat/PecheFantome/data/Zones Protegees MPO/DFO_MPA_MPO_ZPM.shp’
	pass

