from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserLoginRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['mail', 'password']

class FindUserByMailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['mail', 'pk']