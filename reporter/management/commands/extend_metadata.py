# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from hs_core.models import BaseResource
from hs_core.hydroshare.utils import get_resource_by_shortkey
from pprint import pprint
"""
{
 'eastlimit': -111.732,
 'northlimit': 40.829,
 'projection': 'WGS 84 EPSG:4326',
 'southlimit': 40.767,
 'units': 'Decimal degrees',
 'westlimit': -111.819
 }


{
 'east': -111.233445,
 'north': 43.1111,
 'projection': 'WGS 84 EPSG:4326',
 'units': 'Decimal degrees'
 }

  def handle(self, *args, **options):
        lat = options['latitude']
        long = options['longitude']
        start = time.time()
        list_huc4s = []
        point = GEOSGeometry('POINT(%s %s)' % (lat, long))
        pprint(point)
        exit
        huc2_objects = HUC2.objects.filter(geometry__contains=point)
        for huc2 in huc2_objects:
            h4s = huc2.huc4.filter(geometry__contains= point).values()
            list_huc4s.extend(h4s)
        finish = time.time()
        print("The total time taken is {}".format(finish-start))

"""
def read_HUC_data(path):
    total_shapedirs = [ 'WBD_shapefiles/Shape 6/', 'WBD_shapefiles/Shape/',  'WBD_shapefiles/Shape 5/',
                            'WBD_shapefiles/Shape 2/', 'WBD_shapefiles/Shape 3/','WBD_shapefiles/Shape 4/']
    total_shapedirs = [ n+"/WBDHU8.shp" for n in total_shapedirs]
    for dir_name in total_shapedirs:
        print("Performing operation on " + dir_name)
        gdf = gp.read_file(dir_name)
        for _, rows in gdf.iterrows():
            name = rows["Name"]
            tnmid = rows["TNMID"]
            huc8_id = rows["HUC8"]
            geometry_str = str( MultiPolygon([rows['geometry']]) )
            pprint(geometry_str)
            exit
            try:
                geometry = GEOSGeometry(geometry_str)
            except (TypeError, ValueError) as exec:
                print( exec )
                exit
            
            try:           
                #print("The HUC8 id that we are searching for is: "+ huc8_id[0:6]+ " from "+huc8_id)
                huc6 = HUC6.objects.get(huc6_id = huc8_id[0:6])
                HUC8.objects.create( name=name, geometry = geometry, huc8_id=huc8_id, tnmid=tnmid, huc6=huc6)
            except BaseException as exec:
                print( exec )
                exit


def index_resource(r):
    """ index a resource with computed metadata """
    # prints everything you might take into account when computing HUC metadata. 
    if r.metadata:   # a small number of objects don't have any metadata.  
        print("computing metadata for resource {}".format(r.short_id))
        if r.resource_type != 'CompositeResource':
            for c in r.metadata.coverages.all():
                if c.type == 'point': 
                    print("whole resource coverage of type {}".format(c.type))
                    value = c.value
                    # use your code to compute all HUC codes that are relevant. 
                    point = GEOSGeometry('POINT(%s %s)' % (value.east , value.north))
                    
                if c.type == 'box':

        else:  # it's a Composite Resource  
            for lfo in r.logical_files:
                if lfo.metadata:
                    for c in lfo.metadata.coverages.all():
                        if c.type == 'point' or c.type == 'box':
                            value = c.value
                            print("logical file coverage of type {}".format(c.type))
                            pprint(value)
                            # use your code to compute all HUC codes that are relevant.
    else:
        print("resource {} has no metadata".format(r.short_id))

class Command(BaseCommand):
    help = "Computed extended metadata for discovery"

    def add_arguments(self, parser):
        # a list of resource id's, or none to check all resources
        parser.add_argument('resource_ids', nargs='*', type=str)

    def handle(self, *args, **options):
        if len(options['resource_ids']) > 0:  # an array of resource short_id to check.
            for rid in options['resource_ids']:
                try:
                    resource = get_resource_by_shortkey(rid)
                except BaseResource.NotFoundException:
                    msg = "resource {} not found".format(rid)
                    print(msg)
                    continue
                index_resource(resource)
        else:  # check all resources
            print("Indexing all resources")
            for r in BaseResource.objects.all():
                try:
                    resource = get_resource_by_shortkey(r.short_id)
                except BaseResource.NotFoundException:
                    msg = "resource {} not found".format(r.short_id)
                    print(msg)
                    continue
                index_resource(resource)