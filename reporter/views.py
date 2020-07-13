from django.http import JsonResponse
from django.contrib.gis.geos import GEOSGeometry
from reporter.models import HUC2, HUC4, HUC6, HUC8 
from shapely.geometry import Polygon, Point
from django.views.decorators.csrf import csrf_exempt
import json
from pprint import pprint

@csrf_exempt
def handle_point(request):
    json_data = json.loads(request.body.decode('utf-8'))
    long=json_data.get("east")
    lat= json_data.get("north")
    point = GEOSGeometry(Point(lat, long).wkt)
    huc = HUC8.objects.filter(geometry__contains=point)
    if len(huc) == 1:
        return JsonResponse({"HUC8 ID": huc.first().huc_id})
    else:
        return JsonResponse({"message": "Could not find the HUC ID of the point"})

@csrf_exempt
def handle_points(request):
    json_data = json.loads(request.body.decode('utf-8'))
    list_points = json_data.get("list_points")
    answer = []
    for point in list_points:
        long = point["east"]
        lat = point["north"]
        point_data = GEOSGeometry(Point(lat, long).wkt)
        huc = HUC8.objects.filter(geometry__contains=point_data)
        if len(huc) == 1:
            answer.append({"HUC8 ID": huc.first().huc_id})
        else:
            answer.append({"message": "Could not find the HUC ID of the point"})
    return JsonResponse({"list_points": answer})

@csrf_exempt
def handle_polygon(request):
    JsonResponse({"point": 3})

@csrf_exempt
def handle_polygons(request):
    JsonResponse({"point": 3})
