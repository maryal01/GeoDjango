from django.core.management.base import BaseCommand, CommandError
from reporter.models import HUC2, HUC4, HUC6, HUC8
import os, time
from django.contrib.gis.geos import fromstr, Polygon, GEOSGeometry 
import geopandas as gp
from shapely.geometry import Polygon, Point, box
from pprint import pprint

class Command(BaseCommand):
    
    def add_arguments(self, parser):
        parser.add_argument('latitude', type=str, help='latitude of that point')
        parser.add_argument('longitude', type=str, help="longitude of that point")

    def handle(self, *args, **options):
        lat = options['latitude']
        long = options['longitude']
        point = GEOSGeometry(Point(lat, long).wkt)
        huc2 = HUC6.objects.filter(geometry__contains=point)
        print(len(huc2))
        print(huc2.first().huc_id)
        # huc4 = huc2.huc4.filter(geometry__contains= point)[0]
        # print(huc4.huc_id)
