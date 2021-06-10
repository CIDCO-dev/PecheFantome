import shapefile

sf = shapefile.Reader("/home/pat/test/PecheFantome/data/Zones Protegees MPO/DFO_MPA_MPO_ZPM.dbf") 
shapes = sf.shapes()
#for area in shapes:
#	print(area)

#print(len(shapes))
#print(type(shapes))
#print(sf.bbox[0])

for i in range(len(shapes)):
	s = sf.shape(i)
	print(['%.3f' % coord for coord in s.bbox])
