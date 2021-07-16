import atlantis

"""
#usage
test = query_DB("trap") # creation objet query_DB
area = test.get_areas('Casiers perdus','Casiers de peche au crabe perdus')	# methode
data = test.export_to(area,"xml")
print(data)
"""

casiers = atlantis.query_DB("trap")
area = casiers.get_areas('Casiers perdus','Casiers de peche au crabe perdus')
data = casiers.export_to(area,"xml")
print(data)
