from django.conf.urls import include,url
from api import views
from django.urls import path
urlpatterns = [
    path('downward_traversal', views.downwardHUC.as_view(), name="downward"),
    path('upward_traversal', views.upwardHUC.as_view(), name="upward")
]
