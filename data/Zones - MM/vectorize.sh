
# glm
# vectorize a raster layer into probability distribution contours using a 0.0001


for f in `ls b/*.tif`;do
	echo $f
	gdal_contour -b 1 -a ELEV -i 0.0001 -f "ESRI Shapefile" $f b/vectors/`basename $f`.shp
done
