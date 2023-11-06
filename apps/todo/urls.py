from django.urls import path
from rest_framework import routers
from apps.todo.views import TodoViewset

router = routers.DefaultRouter()
router.register('todo', TodoViewset)