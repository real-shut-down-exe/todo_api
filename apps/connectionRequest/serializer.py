from rest_framework import serializers
from .models import ConnectionRequest

class ConnectionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectionRequest
        fields = '__all__'

class MyCustomSerializer(serializers.Serializer):
    sender = serializers.CharField()

class ReceiverSerializer(serializers.Serializer):
    receiver = serializers.CharField()