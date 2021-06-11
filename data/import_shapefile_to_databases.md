#command natif dans Linux/GNU Debian pour importer un shapefile(.shp ) dans une base de données MySQL/MariaDB

#native command in Linux/GNU Debian to import a shapefile( .shp ) in a MySQL/MariaDB Database

ogr2ogr -f "MySQL"   MYSQL:"MyDB,host=HOST,user=USER,password=PASSWORD,port=3306" -a_srs "EPSG:4326" /PATH/FILENAME.shp -skipfailures
