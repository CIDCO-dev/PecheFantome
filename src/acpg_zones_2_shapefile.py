import shapefile

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

	
def ecriture_polygon_2shp(dic,filename):
	nb_element = len(dic)
	liste_element = list(dic)

	w = shapefile.Writer(filename)
	w.field('name','c','40')
	for element in liste_element:
		coordinates = dic[element]
		w.poly([coordinates])
		w.record(element)
	w.close()

def ecriture_points_2shp(liste_points,filename):
	w = shapefile.Writer(filename)
	w.field('name', 'C')
	w.multipoint(liste_points)
	w.record('multipoint')
	w.close()

def Lat_Long_2_x_y(latitude,longitude):
	y = latitude
	x = longitude
	return x,y

def changer_direction(coord):
	coord = coord * -1
	return coord

#coordonnes (non-valide)
"""
coordinates = [(47.937,-65.303),(47.907,-65.303),(48.105,-64.600),(48.201,-64.600)],[(48.267,-64.552),(48.159,-64.552),(48.303,-64.337),(48.303,-64.352)],[(48.460,-63.811),(48.118,-64.000),(48.118,-63.750),(48.460,-63.471)],[(47.763,-63.306),(47.220,-63.306),(47.220,-63.142),(47.763,-63.142)],[(47.591,-62.568),(47.011,-62.637),(47.011,-62.439),(47.591,-62.432)]
"""
#print(coordinates[0])# return liste of point
#print(coordinates[0][0]) # return pair (x,y)
#print (coordinates[0][0][0]) # return x or y

zones = ['Baie des chaleurs','Canal de Grande-Rivière','Nord Shediac Valley','Western Bradelle Valley','Eastern Bradelle Valley']

sud_coordinates = [("47°56’13’’","65°18’01’’"),("47°54’25’’","65°18’01’’"),("48°06’18’’","64°36’00’’"),("48°12’03’’","64°36’00’’")],[("48°16’01’’","64°33’07’’"),("48°09’32’’","64°33’07’’"),("48°06’18’’","64°20’13’’"),("48°18’10’’","64°21’07’’")],[("48°27’36’’","63°48’39’’"),("48°07’04’’","64°00’00’’"),("48°07’04’’","63°45’00’’"),("48°27’36’’","63°25’15’’")],[("47°45’46’’","63°18’21’’"),("47°13’12’’","63°18’21’’"),("47°13’12’’","63°08’31’’"),("47°45’46’’","63°08’31’’")],[("47°35’27’’","62°34’04’’"),("47°01’00’’","62°38’13’’"),("47°01’00’’","62°26’20’’"),("47°35’27’’","62°25’55’’")]


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

# creation du shapefile pour les zones de l'acpg
"""
#inverser x & y de tous les points de la liste de liste de tuple 
new_sud_coordinates = []
polygone = []
for zone in sud_coordinates:
	for point in zone:
		latitude = point[0]
		longitude = point[1]
		#print(x,y)
		x,y = Lat_Long_2_x_y(latitude,longitude)
		point = list(point)
		point[0] = x
		point[1] = y
		polygone += [tuple(point)]
	new_sud_coordinates += [polygone]
	polygone = []
sud_coordinates = new_sud_coordinates

#convertir tous les points en degree decimal
acpg_zones={}
coordinates = []
deg_coordinates = []
for zone in sud_coordinates:
	
	for coord in zone:
		x = coord[0]
		y = coord[1]
		x,y = sud2deg(x,y)
		x = changer_direction(x)
		coordinate = x,y
		coordinates += [coordinate]
	deg_coordinates += [coordinates]
	coordinates = []

#ecrire les polygons dans un fichier .shp
for i in range(len(zones)):
	acpg_zones.update({zones[i] : deg_coordinates[i]})
#print(acpg_zones)
ecriture_polygon_2shp(acpg_zones,"zone_de_peche_acpg.shp")
#print(acpg_zones)

"""
