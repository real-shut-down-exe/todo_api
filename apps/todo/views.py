from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from apps.todo.models import Todo
from apps.todo.serializer import serializer

class TodoControllers(APIView):
    serializer = serializer()

    @api_view(['GET'])
    def SingleGet(self, pk):
        
        try:
            todo_item = Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializer(todo_item)
        return Response(serializer.data)
    
    @api_view(['Get'])
    def MultipleGet(self):
        
        try:
            todo_item_list = Todo.objects#.filter(is_deleted=False)
        except Todo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serialiazer = serializer(todo_item_list, many=True)
        return Response(serialiazer.data)

    @api_view(['POST'])
    @swagger_auto_schema(
    operation_summary="Kullanıcıyı getir",
    operation_description="Belirtilen kullanıcının ayrıntılarını getirir.",
    responses={status.HTTP_200_OK: "Başarılı", status.HTTP_404_NOT_FOUND: "Kullanıcı bulunamadı"}
)
    def Add(form):
        
        serializer = serializer(data = form.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @api_view(['PUT'])
    def Update(form, pk):
        
        try:
            todo_item = Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializer(todo_item, data=form.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @api_view(['Delete'])
    def Delete(self, pk):
        
        try:
            todo_item = Todo.objects.get(pk=pk)
            if todo_item.is_deleted == True:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except Todo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        todo_item.is_deleted = True
        todo_item.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
