from django.urls import include, path
from rest_framework import routers
from .views import UserViewset

routerUrl = routers.DefaultRouter()
routerUrl.register('user', UserViewset)


