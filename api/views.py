from django.http import JsonResponse
from django.contrib.gis.geos import GEOSGeometry
from api.models import HUC2, HUC4, HUC6, HUC8 
from shapely.geometry import Polygon, Point
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
import json
from pprint import pprint


class downwardHUC(APIView):
    def post(self, request):
        list_regions = json.loads(request.body.decode('utf-8')).get("resource_list")
        HUC = 8              #tracks the huc level we are working on
        resources = { }      #tracks the number of resources at a huc level
        hucObj_dic = {
            2: HUC2.objects,
            4: HUC4.objects,
            6: HUC6.objects,
            8: HUC8.objects }
    
        for r in list_regions:
            
            ########## creating the region object with provided latitude and longitude
            region = None
            if r["type"] == "BOX": 
                l_lat, h_lat, l_long, h_long, _ = r.values()
                region = GEOSGeometry('POLYGON((%s %s, %s %s, %s %s, %s %s, %s %s))' % 
                            (h_lat, h_long, h_lat, l_long, l_lat, l_long, l_lat, h_long, h_lat,h_long))
            elif r["type"] == "POINT":
                lat, long, _ = r.values()
                region = GEOSGeometry(Point(lat, long).wkt)
            else:
                print("INVALID region type. box and point are accepted types")
                continue
            #########

            
            ########## storing the intersected regions for the new created region
            intresected_regions = hucObj_dic[HUC].filter(geometry__intersects=region)
            for h in intresected_regions:
                HUCstr = "HUC{}".format(HUC)
                resources[ h[HUCstr] ] = resources.get(h[HUCstr], 0) + 1 
            #########

            
            ########## going downward to the resources where the total regions resource covers is less than 5
            while ( (len(resources.keys()) < 5) and (HUC > 2)):
                HUC /= 2
                resources = { k[:-2]:v for k,v in resources.items() }
            #########
        return intresected_regions.keys()

class upwardHUC(APIView):
    def post(self, request):
        list_regions = json.loads(request.body.decode('utf-8')).get("resource_list")
        HUC = 2              #tracks the huc level we are working on
        resources = []       #tracks the number of resources at a huc level
        hucObj_dic = {
            2: HUC2.objects,
            4: HUC4.objects,
            6: HUC6.objects,
            8: HUC8.objects }
        
        while ( (len(resources) < 5) and (HUC < 16)):
            resources = []
            for r in list_regions: 
                ##########creating the region object with provided latitude and longitude
                region = None
                if r["type"] == "BOX": 
                    l_lat, h_lat, l_long, h_long, _ = r.values()
                    region = GEOSGeometry('POLYGON((%s %s, %s %s, %s %s, %s %s, %s %s))' % 
                                (h_lat, h_long, h_lat, l_long, l_lat, l_long, l_lat, h_long, h_lat,h_long))
                elif r["type"] == "POINT":
                    lat, long, _ = r.values()
                    region = GEOSGeometry(Point(lat, long).wkt)
                else:
                    print("INVALID region type. box and point are accepted types")
                    continue
                #########

                
                ##########storing the intersected regions for the new created region
                intresected_regions = hucObj_dic[HUC].filter(geometry__intersects=region)
                resources = [ r[ "HUC{}".format(HUC) ]  for r in intresected_regions ]
                #########
                print(intresected_regions)
            HUC *=  2
        
        return intresected_regions.keys()