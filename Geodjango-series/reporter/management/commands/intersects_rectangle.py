from django.core.management.base import BaseCommand, CommandError
from reporter.models import HUC2, HUC4
import os, time
from django.contrib.gis.geos import fromstr, Polygon, GEOSGeometry 
import geopandas as gp
from shapely.geometry import Polygon, Point, box
from pprint import pprint

class Command(BaseCommand):
    help = 'Takes in the rectangle and returns the HUC8 region that contains the rectangle'

    def add_arguments(self, parser):
        parser.add_argument('high_lat', type=str, help= "latitude of the rectangle, the larger one")
        parser.add_argument('low_lat', type=str, help="latitude of the rectangle, the smaller one")
        parser.add_argument('high_long', type=str, help="longitude of the rectangle, the higher one")
        parser.add_argument('low_long', type=str, help="longitude of the rectangele, the smaller one")
    
    def handle(self, *args, **options):
        high_lat = options['high_lat']
        low_lat = options['low_lat']
        high_long = options['high_long']
        low_long = options['low_long']

        start = time.time()
        list_intersections = []
        rectangle = GEOSGeometry('POLYGON((%s %s, %s %s, %s %s, %s %s, %s %s))' % (high_lat,high_long, high_lat, low_long, low_lat, low_long, low_lat, high_long, high_lat,high_long))
        
        huc2_objects = HUC2.objects.filter(geometry__rectangle=rectangle)
        for huc2 in huc2_objects:
            huc4_objects = huc2.huc4.objects.filter(geometry_intersects=rectangle)
            for huc4 in huc4_objects:
                huc6_objects = huc4.huc6.objects.filter(geometry_intersects=rectangle)
                list_intersections.extend(huc6_objects.values())
        finish = time.time()
        print("The time took: " + str(finish-start))
        return list_intersections