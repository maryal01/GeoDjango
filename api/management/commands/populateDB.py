from django.core.management.base import BaseCommand, CommandError
from reporter.models import HUC2, HUC4, HUC6, HUC8
import os
import geopandas as gp
from shapely.geometry import MultiPolygon
from django.contrib.gis.geos import GEOSGeometry 
class Command(BaseCommand):
    def handle(self, *args, **options):
        state_names = ["Alaska", "Alabama", "Arkansas", "American_Samoa", "Arizona", "California", 
            "Colorado", "Connecticut", "District_of_Columbia", "Commonwealth_of_the_Northern_Mariana_Islands", 
            "Delaware", "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", 
            "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", 
            "Mississippi", "Montana", "North_Carolina", "North_Dakota", "Nebraska", "New_Hampshire", "New_Jersey", 
            "New_Mexico", "Nevada", "New_York", "Northern_Mariana_Islands","Ohio", "Oklahoma", "Oregon", "Pennsylvania", 
            "Puerto_Rico", "Rhode_Island", "South_Carolina", "South_Dakota", "Tennessee", "Texas", "Utah", "Virginia", 
            "United_States_Virgin_Islands", "Vermont", "Washington", "Wisconsin", "West_Virginia", "Wyoming"]
        test_state_names = ["Arizona", "Iowa", "Kansas", "Kentucky", "Michigan"]
        
        levels = { 2 : HUC2, 4 : HUC4, 6 : HUC6, 8 : HUC8 }
        for hnum in levels.keys():
            for state in test_state_names:
                path = os.path.join('state-files', state, "Shape/WBDHU{}.shp".format(hnum))
                gdf = gp.read_file(path)
                for _, rows in gdf.iterrows():
                    name, tnmid  = rows["Name"], rows["TNMID"]
                    huc_id = rows["HUC{}".format(hnum)]
                    geometry = rows["geometry"]
                    geometry = MultiPolygon([geometry]) if geometry.type == 'Polygon' else geometry
                    multi_polygon = GEOSGeometry(geometry.wkt)
                    print("{}".format(name))
                    if hnum == 2:
                        print("Proceeding to save the huc 2 id")
                        huc = HUC2(name=name, geometry = multi_polygon, huc_id=huc_id, tnmid=tnmid)
                        huc.save()
                        print("Saved the huc 2 id")
                    else:
                        try:
                            lower_huc = levels[hnum - 2].objects.get(huc_id = huc_id[0 : hnum - 2])   
                            huc = levels[hnum](name=name, geometry = multi_polygon, huc_id=huc_id, tnmid=tnmid, lower_huc=lower_huc)
                            huc.save()
                        except BaseException as exec:
                            print(exec)
                            exit