from django.urls import path
from . import views

urlpatterns = [
    path("devices/", views.devices, name="devices"),
    path("ports/", views.ports, name="ports"),
    path("traffic/", views.traffic, name="traffic")
    # path("firewall/", views.firewall, name="firewall"),
]
