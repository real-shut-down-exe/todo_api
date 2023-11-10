from django.urls import include, path
from rest_framework import routers
from .views import ConnectionRequestViewset

routerConnectionRequest = routers.DefaultRouter()
routerConnectionRequest.register('connectionRequest', ConnectionRequestViewset)
