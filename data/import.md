ogr2ogr -f "MySQL"   MYSQL:"MyDB,host=HOST,user=USER,password=PASSWORD,port=3306" -a_srs "EPSG:4326" ‘/home/pat/PecheFantome/data/Zones Protegees MPO/DFO_MPA_MPO_ZPM.shp’ -skipfailures
