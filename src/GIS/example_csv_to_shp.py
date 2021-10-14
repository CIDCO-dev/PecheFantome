import csv
import GGlib

liste_coord = []
coordinates = []
with open('data_for_example/Baiedeschaleurs.csv') as csvfile:
	data = csv.reader(csvfile, delimiter=' ', quotechar='|')
	for row in data:
		# print(row[0])
		coord = row[0].split(",")
		latitude = float(coord[0])
		longitude = float(coord[1])
		coordinates += [latitude, longitude]
		liste_coord += [coordinates]
		coordinates = []
GGlib.ecriture_points_2shp(liste_coord, "test.shp")
