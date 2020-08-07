from django.conf.urls import include,url
from reporter import views
urlpatterns = [
    url(r'^handle_point/', views.handle_point),
    url(r'^handle_points/', views.handle_points),
    url(r'^handle_polygon/', views.handle_polygon),
    url(r'^index/', views.index),
    url(r'^handle_polygons/', views.handle_polygons),
]
