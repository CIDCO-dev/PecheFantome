import csv
import tqdm
import os
import subprocess
import tqdm


def readFile_index():
	filename_list = []
	with open('mammal/akernel_density.csv', newline='') as csvfile:
		csvfile = csv.reader(csvfile, delimiter=',', quotechar='"')
		for row in csvfile:
		    if (len(row ) > 0):
		    	filename_list.append(row[0])
	filename_list.remove('data')
	filename_list.remove('mammals')
	filename_list.pop()
	#print(filename_list)
	#print(len(filename_list))
	return filename_list
	
name_list = readFile_index()
#print(name_list)

def extract_contour(inputFilePath, outputPath, fileName):
	gdal_contour = "/usr/bin/gdal_contour"
	if not os.path.exists(inputFilePath):
		print("input File Path does not exist")
		return False
	directoryName = os.path.basename(inputFilePath)
	directory = directoryName[:-4]
	outputPath = os.path.join(outputPath,directory)
	if not os.path.exists(outputPath):
		os.mkdir(outputPath)
	fileName = fileName + ".shp"
	outputPath = os.path.join(outputPath, fileName)
	export = subprocess.Popen([gdal_contour, "-a", "sightings", "-i", "1", "-f", "ESRI Shapefile", inputFilePath, outputPath])
	export.wait()
	return True


"""
inputFilePath = "mammal/KD3.tif"
outputPath = "./"
fileName = name_list[1]

status = extract_contour(inputFilePath,outputPath,fileName)
if(status == True):
	print("done")
"""

def export2DB(filePath):
	ogr2ogr = "/usr/bin/ogr2ogr"
	#ogr2ogr -f "MySQL"   MYSQL:"crabnet,host=localhost,user=admin,password=jmlespatate,port=3306" -a_srs "EPSG:4326" ‘/home/pat/PecheFantome/data/Zones Protegees MPO/DFO_MPA_MPO_ZPM.shp’
	export = subprocess.Popen([ogr2ogr, "-f", "MYSQL", "MYSQL:crabnet,host=localhost,user=admin,password=jmlespatate,port=3306", "-a_srs", "EPSG:4326", filePath])
	if (export.wait() != 0):
		return False
	else:
		return True

"""
status = export2DB()
if(status == True):
	print("export to db done")
"""
tif_fileList = []
tifs_path = "./mammal"
for tif in os.listdir(tifs_path):
	if tif.endswith(".tif"):
		tif_fileList.append(tif)
tif_fileList.sort()
tif_fileList.remove("KD_all_mammals.tif")
print(tif_fileList)

for i in range(len(tif_fileList)):
	index = tif_fileList[i]
	index = index[2:-4]
	index = int(index)-2
	output_fileName = name_list[index]
	outputPath = "."
	input_file = os.path.join("./mammal",tif_fileList[i])
	if (extract_contour(input_file, outputPath, output_fileName)):
		print(output_fileName, " created")
	path = tif_fileList[i]
	path = path[:-4]
	output_fileName += ".shp"
	shapefile_path = os.path.join(path,output_fileName)
	
	if(export2DB(shapefile_path)):
		print(shapefile_path, " exported")

