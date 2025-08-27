from django.contrib import admin
from django.urls import path, include
from networktool import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.devices),  # home page → devices
    path("", include("networktool.urls")),
]
