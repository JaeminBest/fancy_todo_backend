from django.conf.urls import url, include 
from django.contrib import admin
from django.urls import path

from .views import *

# Routers provide an easy way of automatically determining the URL conf.

urlpatterns = [
    path('todo/', todo_endpoint),
    path('healthcheck/',healthcheck)
]