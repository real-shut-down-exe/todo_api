from rest_framework import viewsets
from apps.todo.models import Todo
from apps.todo.serializer import TodoSerializer

class TodoViewset(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
