from django.core.management.base import BaseCommand, CommandError
from reporter.models import HUC2, HUC4, HUC6, HUC8

import os
import geopandas as gp
from shapely.geometry import Polygon, Point, box, MultiPolygon
from django.contrib.gis.geos import fromstr, Polygon, GEOSGeometry 

class Command(BaseCommand):
    def handle(self, *args, **options):
        total_shapedirs = ['WBD_shapefiles/Shape 6/', 'WBD_shapefiles/Shape/','WBD_shapefiles/Shape 5/','WBD_shapefiles/Shape 2/','WBD_shapefiles/Shape 3/','WBD_shapefiles/Shape 4/']
        total_shapedirs = [ n+"/WBDHU8.shp" for n in total_shapedirs]
        for dir_name in total_shapedirs:
            print("Performing operation on " + dir_name)
            gdf = gp.read_file(dir_name)
            for index, rows in gdf.iterrows():
                name = rows["Name"]
                tnmid = rows["TNMID"]
                huc8_id = rows["HUC8"]
                geometry_str = str( MultiPolygon([rows['geometry']]) )
                try:
                    geometry = GEOSGeometry(geometry_str)
                except (TypeError, ValueError) as exec:
                    print("error")
                    continue
                try:           
                    print("The HUC8 id that we are searching for is: "+ huc8_id[0:6]+ " from "+huc8_id)
                    huc6 = HUC6.objects.get(huc6_id = huc8_id[0:6])
                    HUC8.objects.create( name=name, geometry = geometry, huc8_id=huc8_id, tnmid=tnmid, huc6=huc6)
                except:
                    print("Error Storing")

#skipped HUC2 files -- shape, shape 5
#skipped HUC4 files -- 3 from shape 6 and all of shape and shape 5