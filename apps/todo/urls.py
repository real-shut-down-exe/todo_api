from django.urls import path
from apps.todo.views import TodoControllers

urlpatterns = [
    path('multipleget/',TodoControllers.MultipleGet, name='MultipleGet'),
    path('singleget/<int:pk>/',TodoControllers.SingleGet, name='SingleGet'),
    path('add/',TodoControllers.Add, name='Add'),
    path('update/<int:pk>/',TodoControllers.Update, name='Update'),
    path('delete/<int:pk>/',TodoControllers.Delete, name='Delete'),
]