from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
import json

from apps.user.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken

from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    print(refresh)
    print(refresh.access_token)
    return {
        "refresh":str(refresh),
        "access": refresh.access_token,
    }


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['role'] = user.role
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class UserSerializer(ModelSerializer):  
    class Meta:
        model = User
        fields = ['username','email','password']

class CreateUserApiView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token=  get_tokens_for_user(user)
            return Response(str(token),status.HTTP_201_CREATED)


    