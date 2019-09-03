from django.contrib import admin
from .models import HUC2, HUC4, HUC6, HUC8
#from django.contrib.gis.db import OSMGeoAdmin
from leaflet.admin import LeafletGeoAdmin

admin.site.register(HUC2)
admin.site.register(HUC4)
admin.site.register(HUC6)
admin.site.register(HUC8)
