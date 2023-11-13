from rest_framework import viewsets
from apps.todo.models import Todo
from apps.todo.serializer import TodoSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema


class TodoViewset(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    @action(detail=False, methods=["post"])
    def get_all_todo_by_id(self, request):
        try:
            pk = request.data.get("created_by")

            todos = Todo.objects.filter(created_by=pk)
            todo_list = []

            if todos.exists():
                pass
                for todo in todos:
                    todo_info = {
                        "title": todo.title,
                        "is_deleted": todo.is_deleted,
                        "id": todo.pk,
                        "created_at": todo.created_at,
                    }
                    todo_list.append(todo_info)
            else:
                pass
            return Response(todo_list, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": "Your password or email is incorrect or this mail is in use"},
                status=400,
            )
        
    @action(detail=False, methods=["post"])
    def DescTodo(self, request):
        try:
            todos = Todo.objects.filter(created_by=1).order_by('created_at')
            serializer = TodoSerializer(todos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "Your password or email is incorrect or this mail is in use"},
                status=400,
            )
        
    @action(detail=False, methods=["post"])
    def AscTodo(self, request) :
        try:
            todos = Todo.objects.filter(created_by=1).order_by('-created_at')
            serializer = TodoSerializer(todos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "Your password or email is incorrect or this mail is in use"},
                status=400,
            )