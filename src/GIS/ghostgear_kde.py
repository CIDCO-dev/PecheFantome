import csv
import os
import subprocess
from tqdm import tqdm
import GGlib
"""
def readFile_index():
	filename_list = []
	with open('../../data/gear_kernels/ggkde.csv', newline='') as csvfile:
		csvfile = csv.reader(csvfile, delimiter=',', quotechar='"')
		for row in csvfile:
		    if (len(row) > 0):
		    	filename_list.append(row[0])
	return filename_list
	
#print(readFile_index())
"""

file_path = "/home/pat/projet/PecheFantome/data/gear_kernels/proccessed"

def list_dir():
	filename_list = []
	shpFolder_list = []
	for Files in tqdm(os.listdir(file_path)):
		if Files.endswith(".tif"):
			filename_list.append(Files)
			shpFolder= Files[3:-4]
			shpFolder_list.append(shpFolder)
	return filename_list, shpFolder_list

filename_list, shpFolder_list = list_dir()
print(filename_list, shpFolder_list)

outputPath = "/home/pat/projet/PecheFantome/data/gear_kernels/proccessed/shapefile"
if(len(filename_list) != len(shpFolder_list)):
	print("error ! len(filename_list) != len(shpFolder_list)")
else:
	for i in range(len(filename_list)-1):
		filePath = os.path.join(file_path,filename_list[i])
		if(GGlib.extract_contour_Tiff_2_Shp(filePath, outputPath, shpFolder_list[i]) == False):
			print("error extracting contour")
		else:
			print("shapefile created :", shpFolder_list[i])
			path = os.path.join(outputPath,filename_list[i][:-4])
			path = os.path.join(path, shpFolder_list[i] + ".shp")
			print(path)
			if(GGlib.export_Shp2DB(path)):
				print("shapefile exported: ", shpFolder_list[i])
			else:
				print("error exporting to DB")
