import Atlantis


"""
db = Atlantis.GGDB()
result = db.query("trap")
#print(result)
gpx = db.dfo_engins2GPX("test","testing")
print(gpx)

db2 = Atlantis.GGDB()
result = db.query("show tables")
print(result)
result = db2.query("select * from acpg")
print(result)
"""
db3 = Atlantis.GGDB()
result = db3.extractSHP("acpg", "'Baie_des_chaleurs'")
print(result)
