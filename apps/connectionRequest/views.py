from rest_framework import viewsets
from .models import ConnectionRequest
from .serializer import ConnectionRequestSerializer

class ConnectionRequestViewset(viewsets.ModelViewSet):
    queryset = ConnectionRequest.objects.all()
    serializer_class = ConnectionRequestSerializer
