from django.core.management.base import BaseCommand, CommandError
from reporter.models import HUC2, HUC4, HUC6, HUC8

import geopandas as gp
from shapely.geometry import MultiPolygon
from django.contrib.gis.geos import fromstr 
class Command(BaseCommand):
    def handle(self, *args, **options):
        total_shapedirs = [ 'WBD_shapefiles/Shape 6/', 'WBD_shapefiles/Shape/',  'WBD_shapefiles/Shape 5/',
                            'WBD_shapefiles/Shape 2/', 'WBD_shapefiles/Shape 3/','WBD_shapefiles/Shape 4/']
        levels = {2:HUC2, 4:HUC4, 6:HUC6, 8:HUC8}
        for huc_num in [2,4,6,8]:
            print("Inserting huc level {} now".format(str(huc_num)))
            for dir_name in total_shapedirs:
                gdf = gp.read_file("{}WBDHU{}.shp".format(dir_name, str(huc_num)))
                for _, rows in gdf.iterrows():
                    name = rows["Name"]
                    tnmid = rows["TNMID"]
                    huc_id = rows["HUC{}".format(str(huc_num))]
                    geom = rows["geometry"]
                    geometry = None
                    if geom.type == 'MultiPolygon':
                        geometry = fromstr(str(geom))
                    else:
                        multi = MultiPolygon([geom])
                        geometry = fromstr(str(multi))

                    if huc_num == 2:
                        huc = HUC2(name=name, geometry = geometry, huc_id=huc_id, tnmid=tnmid)
                        huc.save()
                    else:
                        try:
                            lower_huc = levels[huc_num-2].objects.get(huc_id = huc_id[0:huc_num-2])   
                            huc = levels[huc_num](name=name, geometry = geometry, huc_id=huc_id, tnmid=tnmid, lower_huc=lower_huc)
                            huc.save()
                        except BaseException as exec:
                            print(exec)
                            exit