from django.core.management.base import BaseCommand, CommandError
from reporter.models import HUC2, HUC4
import os, time
from django.contrib.gis.geos import fromstr, Polygon, GEOSGeometry 
import geopandas as gp
from shapely.geometry import Polygon, Point, box


class Command(BaseCommand):
    
    def add_arguments(self, parser):
        parser.add_argument('latitude', type=str, help='latitude of that point')
        parser.add_argument('longitude', type=str, help="longitude of that point")

    def handle(self, *args, **options):
        lat = options['latitude']
        long = options['longitude']
        start = time.time()
        list_huc4s = []
        point = GEOSGeometry('POINT(%s %s)' % (lat, long))
        huc2_objects = HUC2.objects.filter(geometry__contains=point)
        for huc2 in huc2_objects:
            h4s = huc2.huc4.filter(geometry__contains= point).values()
            list_huc4s.extend(h4s)
        finish = time.time()
        print("The total time taken is {}".format(finish-start))