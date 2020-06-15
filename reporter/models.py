from __future__ import unicode_literals
from django.db import models
from django.contrib.gis.db import models
from django.db.models import Manager as GeoManager

class HUC2(models.Model):
    geometry = models.PolygonField()
    name = models.CharField(max_length=255, null=False, unique=True)
    tnmid = models.CharField(max_length=255, null=False, unique=True)
    huc2_id = models.CharField(max_length=2, null=False, unique=True)
    
    def search_point(self):
        return self.name
    
    def search_rectangle(self):
        return self.name

class HUC4(models.Model):
    geometry = models.PolygonField()
    name = models.CharField(max_length=255, null=False, unique=True)
    tnmid = models.CharField(max_length=255, null=False, unique=True)
    huc4_id = models.CharField(max_length=4, null=False, unique=True) 
    huc2 = models.ForeignKey(HUC2, related_name="huc4", on_delete=models.PROTECT)
    
    def search_point(self):
        return self.name
    
    def search_rectangle(self):
        return self.name

class HUC6(models.Model):
    geometry = models.MultiPolygonField()
    name = models.CharField(max_length=255, null=False, unique=True)
    tnmid = models.CharField(max_length=255, null=False, unique=True)
    huc6_id = models.CharField(max_length=6, null=False, unique=True) 
    huc4 = models.ForeignKey(HUC4, related_name="huc6", on_delete=models.PROTECT)

    def search_point(self):
        return self.name
    
    def search_rectangle(self):
        return self.name
    
    
class HUC8(models.Model):
    geometry = models.MultiPolygonField()
    name = models.CharField(max_length=255, null=False, unique=True)
    tnmid = models.CharField(max_length=255, null=False, unique=True)
    huc8_id = models.CharField(max_length=8, null=False, unique=True) 
    huc6 = models.ForeignKey(HUC6, related_name="huc8", on_delete=models.PROTECT)

    def search_point(self):
        return self.name
    
    def search_rectangle(self):
        return self.name