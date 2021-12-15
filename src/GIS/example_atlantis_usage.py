import Atlantis



#db = Atlantis.GGDB()
#result = db.query("trap")
#print(result)
#gpx = db.toGPX("test","testing")
#print(gpx)
#if(db.importSHP("/home/pat/KD2/megaptera_novaeangliae.shp")):
#	print("done")

#db2 = Atlantis.GGDB(database="Pat_test_DB")
#result = db.query("show tables")
#print(type(result))


db3 = Atlantis.GGDB()
result = db3.extractSHP("acpg", "'Baie_des_chaleurs'")
print(result)
print(type(result))
print(len(result))
