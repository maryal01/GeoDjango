from django.http import JsonResponse
from django.contrib.gis.geos import GEOSGeometry
from api.models import HUC2, HUC4, HUC6, HUC8 
from shapely.geometry import Polygon, Point
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from pprint import pprint

'''
    Expects: list of points and boxes
    Returns: json list of HUC id of the resource containing those points and boxes
    Algorithm: starts from HUC8 ids and moves down to HUC2 ids when the current number 
            of resources that contain a given point or box is more than 5
'''
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
                resources[ h.huc_id ] = resources.get(h.huc_id, 0) + 1 
            #########

            
            ########## going downward to the resources where the total regions resource covers is less than 5
            while ( (len(resources.keys()) > 5) and (HUC > 2)):
                HUC //= 2
                resources = { k[: HUC ]:v for k,v in resources.items() }
            #########
        return Response({ "HUC_ID": resources.keys() })


'''
    Expects: list of points and boxes
    Returns: json list of HUC id of the resource containing those points and boxes
    Algorithm: starts from HUC2 ids and moves up to HUC8 ids when the current number 
            of resources that contain all points or boxes  provided is less than 5
'''
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
            resources = set()
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
                resources.update([ir.huc_id for ir in intresected_regions ])
                #########
            HUC *=  2
        
        return Response({ "HUC_ID": resources })