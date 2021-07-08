import shapefile

#convertir des degrés a des sous-unités du degré 
def deg2sud(x,y):
	if x < 0 :
		x = abs(x)
		directionx = "S"
	else :
		directionx = "N"
	deg = int(x)
	temp = 60 * (x - deg)
	minutes = int(temp)
	seconds = int(60 * (temp - minutes))
	deg = '{}'.format(deg)
	minutes = '{}'.format(minutes)
	seconds = '{}'.format(seconds)
	sudx = deg +"°"+minutes+"’"+seconds+"’’"+directionx

	if y < 0 :
		y = abs(y)
		directiony = "W"
	else :
		directiony = "E"	
	deg = int(y)
	temp = 60 * (y - deg)
	minutes = int(temp)
	seconds = int(60 * (temp - minutes))
	deg = '{}'.format(deg)
	minutes = '{}'.format(minutes)
	seconds = '{}'.format(seconds)
	sudy = deg +"°"+minutes+"’"+seconds+"’’"+directiony
	
	return sudx,sudy
			
#convertir des sous-unités du degré a des degrés 			
def sud2deg(x,y): # le programme prends pour aquis que les coordonnees sont des coordonnees au QC et donc les coordonnees ont des directions (x Nord,y Ouest)
	#print(len(x))
	temp = x.split("°")
	deg = float(temp[0])
	del temp[0]
	x=temp[0]
	temp = x.split("’")
	minutes = float(temp[0])
	secondes = float(temp[1])
	centime = (secondes/3600) + (minutes/60)
	deg = deg + centime
	degx = round(deg,3)
	
	temp = y.split("°")
	deg = float(temp[0])
	del temp[0]
	y=temp[0]
	temp = y.split("’")
	minutes = float(temp[0])
	secondes = float(temp[1])
	centime = (secondes/3600) + (minutes/60)
	deg = (deg + centime) * -1
	degy = round(deg,3)
	
	return degx,degy

	
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

#semblerait qu'on ait pas besoin de boucler la boucle
def test_debut_egal_fin_polygone(dic,key): #non terminer
	coordinates = dic[key]
	nb_points = len(coordinates[0])-1
	if coordinates[0][0] != coordinates[0][nb_points]:
		print("pas bon")
		#fonction test si le points n'est pas dans la liste de points
		#si fonction test == True --> ajouter le premier point a la fin
		#si fonction test == True --> return True
	else:
		#print("premier et dernier point identique")
		return True




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
"""
#ecrire dans un shapefile des polygones a partir d'un dictionaire {zone : coordinate }

acpg_zones = {}
for i in range(len(zones)):
	acpg_zones.update({zones[i] : coordinates[i]})
#print(acpg_zones)
ecriture_polygon_2shp(acpg_zones,"acpg.shp")
"""
#usage 2
#x = sud2deg("47°56’13’’","65°18’01’’")
#print(x)
	
#x = deg2sud(47.937,-65.303)
#print(x)



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
