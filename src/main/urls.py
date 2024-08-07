"""URL configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
https://docs.djangoproject.com/en/5.0/topics/http/urls/
"""

# Third-party dependencies:
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
]
