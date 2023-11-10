from rest_framework import serializers
from .models import ConnectionRequest

class ConnectionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectionRequest
        fields = '__all__'
            