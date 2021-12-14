import Atlantis


"""
db = Atlantis.GGDB()
db.query("trap")
areas = db.toGPX("test","testing")
print(areas)
"""
#db2 = Atlantis.GGDB(host='localhost:3306',user="admin",password="jmlespatate", database = "crabnet")
db = Atlantis.GGDB()
db.importSHP("/home/pat/KD2/megaptera_novaeangliae.shp")
