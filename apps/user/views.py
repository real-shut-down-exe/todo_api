from rest_framework import status
from rest_framework import viewsets
from .models import User
from .serializer import UserSerializer, UserLoginRegisterSerializer, FindUserByMailSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(request_body=UserLoginRegisterSerializer)
    @action(detail=False, methods=['post'])
    def login(self, request):

        try:
            mail = request.data.get('mail', None)
            password = request.data.get('password', None)

            if not mail or not password:
                return Response({'error': 'Email and password are required fields.'}, status=400)
            
            user = User.objects.get(mail=mail).check_password(password, mail)

            if user.status_code == 200:
                user_data = {
                    'mail': user.data.mail,
                    'pk': user.data.pk,
                    }
                return Response(user_data, status=200)
            else:
                return Response({'error': 'Try with valid Email or Password.'}, status=400)
            
        except Exception as e:
            return Response({'error': 'Try with valid Email or Password.'}, status=400)

    @swagger_auto_schema(request_body=UserLoginRegisterSerializer)
    @action(detail=False, methods=['post'])
    def signup(self, request):

        try:
            mail = request.data.get('mail', None)
            password = request.data.get('password', None)

            if not mail or not password:
                return Response({'error': 'Email and password are required fields.'}, status=400)
            
            user = User.objects.filter(mail=mail).first()

            if user is None:
                new_user = User(mail=mail, password=password)
                new_user.save()

                user_data = {
                    'mail': mail,
                    'pk': new_user.pk,
                    }
                
                return Response(user_data, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Your password or email is incorrect or this mail is in use'}, status=400)
            
        except Exception as e:
            return Response({'error': 'Your password or email is incorrect or this mail is in use'}, status=400)
        
    @swagger_auto_schema(request_body = FindUserByMailSerializer)
    @action(detail=False, methods=['post'])
    def findUserByMail(self, request):

        try:
            mail = request.data.get('mail', None)

            if not mail:
                return Response({'error': 'Email required field.'}, status=400)
            
            user = User.objects.filter(mail=mail).first()

            if user.mail == mail:
                user_data = {
                    'mail': user.mail,
                    'pk': user.pk,
                    }
                return Response(user_data, status=200)
            else:
                return Response({'error': 'Try with valid Email or Password.'}, status=400)
        except Exception as e:
            return Response({'error': 'Your password or email is incorrect or this mail is in use'}, status=400)