from __future__ import unicode_literals
from django.db import models
from django.contrib.gis.db import models

class HUC2(models.Model):
    geometry = models.MultiPolygonField()
    name = models.CharField(max_length=255, null=False)
    tnmid = models.CharField(max_length=255, null=False)
    huc_id = models.CharField(max_length=2, null=False, unique=True, primary_key=True)
    

class HUC4(models.Model):
    geometry = models.MultiPolygonField()
    name = models.CharField(max_length=255, null=False)
    tnmid = models.CharField(max_length=255, null=False)
    huc_id = models.CharField(max_length=4, null=False, unique=True, primary_key=True) 
    lower_huc = models.ForeignKey(HUC2, related_name="huc4", on_delete=models.PROTECT)
    

class HUC6(models.Model):
    geometry = models.MultiPolygonField()
    name = models.CharField(max_length=255, null=False)
    tnmid = models.CharField(max_length=255, null=False)
    huc_id = models.CharField(max_length=6, null=False, unique=True, primary_key=True) 
    lower_huc = models.ForeignKey(HUC4, related_name="huc6", on_delete=models.PROTECT)
    
class HUC8(models.Model):
    geometry = models.MultiPolygonField()
    name = models.CharField(max_length=255, null=False)
    tnmid = models.CharField(max_length=255, null=False)
    huc_id = models.CharField(max_length=8, null=False, unique=True, primary_key=True) 
    lower_huc = models.ForeignKey(HUC6, related_name="huc8", on_delete=models.PROTECT)
