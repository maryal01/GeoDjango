from django.http import JsonResponse
from django.contrib.gis.geos import GEOSGeometry
from reporter.models import HUC2, HUC4, HUC6, HUC8 
from shapely.geometry import Polygon, Point
from django.views.decorators.csrf import csrf_exempt
import json
from pprint import pprint

def index(request):
    return JsonResponse({"Test": "Home page"})

@csrf_exempt
def handle_point(request):
    json_data = json.loads(request.body.decode('utf-8'))
    long=json_data.get("longitude")
    lat= json_data.get("latitude")
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
        long = point["longitude"]
        lat = point["latitude"]
        point_data = GEOSGeometry(Point(lat, long).wkt)
        huc = HUC8.objects.filter(geometry__contains=point_data)
        pprint([h.huc_id for h in huc])
        if len(huc) == 1:
            answer.append({"HUC8 ID": huc.first().huc_id})
        else:
            answer.append({"message": "Could not find the HUC ID of the point"})
    return JsonResponse({"list_points": answer})

@csrf_exempt
def handle_polygon(request):
    json_data = json.loads(request.body.decode('utf-8'))
    high_lat = json_data.get("high_latitude")
    low_lat = json_data.get("low_latitude")
    high_long = json_data.get("high_longitude")
    low_long = json_data.get("low_longitude")
    rectangle = GEOSGeometry('POLYGON((%s %s, %s %s, %s %s, %s %s, %s %s))' % 
                (high_lat, high_long, high_lat, low_long, low_lat, low_long, low_lat, high_long, high_lat,high_long))
    huc4_lists = HUC4.objects.filter(geometry__intersects=rectangle)
    huc6_lists = []
    huc8_lists = []
    if len(huc4_lists) <= 5:
        for huc in huc4_lists:
            huc6_lists.append( huc.huc6.objects.filter(geometry__contains=rectangle) )
    else:
        return JsonResponse({"HUC4 ID": [huc.huc_id for huc in huc4_lists]})
    
    if len(huc6_lists) <= 5:
        for huc in huc6_lists:
            huc8_lists.append(huc.huc8.objects.filter(geometry_contains=rectangle))
    else:
        return JsonResponse({"HUC6 ID": [huc.huc_id for huc in huc6_lists]})
    
    if huc8_lists:
        return JsonResponse({"HUC8 ID": [huc.huc_id for huc in huc8_lists]})
    else:
        return JsonResponse({"message": "Could not find the HUC ID of the polygon"})

@csrf_exempt
def handle_polygons(request):
    json_data = json.loads(request.body.decode('utf-8'))
    list_polygons = json_data.get("list_points")
    answer = []
    for polygon in list_polygons:
        high_lat = polygon["high_latitude"]
        low_lat = polygon["low_latitude"]
        high_long = polygon["high_longitude"]
        low_long = polygon["low_longitude"]
        rectangle = GEOSGeometry('POLYGON((%s %s, %s %s, %s %s, %s %s, %s %s))' % 
                    (high_lat, high_long, high_lat, low_long, low_lat, low_long, low_lat, high_long, high_lat,high_long))
        huc4_lists = HUC4.objects.filter(geometry__intersects=rectangle)
        huc6_lists = []
        huc8_lists = []
        if len(huc4_lists) <= 5:
            for huc in huc4_lists:
                huc6_lists.append( huc.huc6.objects.filter(geometry__contains=rectangle) )
        else:
            answer.append({"HUC4 ID": [huc.huc_id for huc in huc4_lists]})
            continue
        
        if len(huc6_lists) <= 5:
            for huc in huc6_lists:
                huc8_lists.append(huc.huc8.objects.filter(geometry_contains=rectangle))
        else:
            answer.append({"HUC6 ID": [huc.huc_id for huc in huc6_lists]})
            continue
        
        if huc8_lists:
            answer.append({"HUC8 ID": [huc.huc_id for huc in huc8_lists]})
        else:
            answer.append({"message": "Could not find the HUC ID of the polygon"})
    return JsonResponse({"list_polygons": answer})
