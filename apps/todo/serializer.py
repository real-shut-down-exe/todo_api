from rest_framework import serializers
from .models import Todo  # Import the Todo model from your app's models

class serializer(serializers.ModelSerializer):
    class Meta:
        class Meta:
            model = Todo
            fields = "__all__"
