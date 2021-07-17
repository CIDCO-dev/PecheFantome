# Importation de données

# Fichiers SHP
## Installation  
Installation de ogr2ogr
apt install gdal-bin

## Importer un shapefile(.shp ) dans une base de données MySQL/MariaDB
ogr2ogr -f "MySQL"   MYSQL:"MyDB,host=HOST,user=USER,password=PASSWORD,port=3306" -a_srs "EPSG:4326" -lco engine=MYISAM /PATH/FILENAME.shp 

