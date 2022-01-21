import shapefile
import csv
import os
import subprocess

#convertir des degrés a des sous-unités du degré 
def deg2sud(latitude,longitude):
	if latitude < 0 :
		latitude = abs(latitude)
		directiony = "S"
	else :
		directiony = "N"
	deg = int(latitude)
	temp = 60 * (latitude - deg)
	minutes = int(temp)
	seconds = int(60 * (temp - minutes))
	deg = '{}'.format(deg)
	minutes = '{}'.format(minutes)
	seconds = '{}'.format(seconds)
	latitude = deg +"°"+minutes+"’"+seconds+'"'+directiony

	if longitude < 0 :
		longitude = abs(longitude)
		directionx = "W"
	else :
		directionx = "E"	
	deg = int(longitude)
	temp = 60 * (longitude - deg)
	minutes = int(temp)
	seconds = int(60 * (temp - minutes))
	deg = '{}'.format(deg)
	minutes = '{}'.format(minutes)
	seconds = '{}'.format(seconds)
	longitude = deg +"°"+minutes+"’"+seconds+'"'+directionx
	
	return latitude,longitude
			
#convertir des sous-unités du degré a des degrés 			
def sud2deg(latitude,longitude): 
	#print(len(x))
	temp = longitude.split("°")
	deg = float(temp[0])
	del temp[0]
	x=temp[0]
	temp = x.split("’")
	minutes = float(temp[0])
	secondes = float(temp[1])
	centime = (secondes/3600) + (minutes/60)
	deg = (deg + centime)
	longitude = round(deg,3)
	
	temp = latitude.split("°")
	deg = float(temp[0])
	del temp[0]
	y=temp[0]
	temp = y.split("’")
	minutes = float(temp[0])
	secondes = float(temp[1])
	centime = (secondes/3600) + (minutes/60)
	deg = (deg + centime)
	latitude = round(deg,3)
	
	return latitude,longitude 

def write_points_2csv(points_list, filename):
	with open(filename+".csv", 'w', newline='') as csvfile:
		file = csv.writer(csvfile, delimiter=",", quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for coord in points_list:
			file.writerow(coord)

# dic = dictionary
# key : string (polygon name), Value (list of point : vertex of polygon)
def write_polygon_2shp(dic,filename):
	liste_element = list(dic)
	w = shapefile.Writer(filename)
	w.field('name','c','40')
	for element in liste_element:
		coordinates = dic[element]
		w.poly([coordinates])
		w.record(element)
	w.close()

def write_points_2shp(liste_points, filename):
	w = shapefile.Writer(filename)
	w.field('name', 'C')
	w.multipoint(liste_points)
	w.record('multipoint')
	w.close()

def Lat_Long_2_x_y(latitude,longitude):
	y = latitude
	x = longitude
	return x,y

def change_direction(coord):
	coord = coord * -1
	return coord

#sudo apt install gdal-bin
def extract_contour_Tiff_2_Shp(inputFilePath, outputPath, fileName):
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



#zones = ['Baie des chaleurs','Canal de Grande-Rivière','Nord Shediac Valley','Western Bradelle Valley','Eastern Bradelle Valley']

#sud_coordinates = [("47°56’13’’","65°18’01’’"),("47°54’25’’","65°18’01’’"),("48°06’18’’","64°36’00’’"),("48°12’03’’","64°36’00’’")],[("48°16’01’’","64°33’07’’"),("48°09’32’’","64°33’07’’"),("48°06’18’’","64°20’13’’"),("48°18’10’’","64°21’07’’")],[("48°27’36’’","63°48’39’’"),("48°07’04’’","64°00’00’’"),("48°07’04’’","63°45’00’’"),("48°27’36’’","63°25’15’’")],[("47°45’46’’","63°18’21’’"),("47°13’12’’","63°18’21’’"),("47°13’12’’","63°08’31’’"),("47°45’46’’","63°08’31’’")],[("47°35’27’’","62°34’04’’"),("47°01’00’’","62°38’13’’"),("47°01’00’’","62°26’20’’"),("47°35’27’’","62°25’55’’")]
#print(coordinates[0])# return list of point
#print(coordinates[0][0]) # return pair (x,y)
#print (coordinates[0][0][0]) # return x or y

#usage 1

#ecrire dans un shapefile des polygones a partir d'un dictionaire {zone : coordinate }
"""
acpg_zones = {}
for i in range(len(zones)):
	acpg_zones.update({zones[i] : coordinates[i]})
#print(acpg_zones)
ecriture_polygon_2shp(acpg_zones,"acpg.shp")
"""

#usage 2
"""
x = sud2deg("65°18’01’’","47°56’13’’")
print(x)

x = deg2sud(47.937,-65.3003)
print(x)
"""


#usage 3
#afficher la conversion de tous les points en degree a partir des coordonnes en sous unite du degree
""" 
print(len(sud_coordinates))
for zone in sud_coordinates:
	print("\n")
	for coord in zone:
		x = coord[0]
		y = coord[1]
		coordinate = sud2deg(x,y)
		print(coordinate)
"""

