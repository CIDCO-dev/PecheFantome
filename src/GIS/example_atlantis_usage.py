import atlantis

area = atlantis.get_elements('Casiers perdus','Casiers de peche au crabe perdus')
atlantis.export_to(area,"shapefile","test")
atlantis.export_to(area,"gpx","test")
atlantis.export_to(area,"csv","trap_location")