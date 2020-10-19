from django.conf.urls import include,url
from api import views
urlpatterns = [
    url(r'^DtraverseHUC/', views.DtraverseHUC),
    url(r'^UtraverseHUC/', views.UtraverseHUC),
    url(r'^index/', views.index),
]
