from rest_framework import viewsets
from .models import User
from .serializer import UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action

class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def check_credentials(self, request):
        mail = request.data.get('mail', None)
        password = request.data.get('password', None)

        if not mail or not password:
            return Response({'error': 'E-posta ve parola gerekli alanlardır.'}, status=400)

        user = User.objects.get(mail=mail)
        a = user.check_password(password)
        if a.status_code == 200:
            return Response({'message': 'Current Usser'}, status=200)
        else:        
            return Response({'error': 'Kullanıcı bulunamadı.'}, status=404)
