from rest_framework import viewsets
from .models import User
from .serializer import UserSerializer, UserLoginSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema

class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(request_body=UserLoginSerializer)
    @action(detail=False, methods=['post'])
    def login(self, request):

        try:
            mail = request.data.get('mail', None)
            password = request.data.get('password', None)

            if not mail or not password:
                return Response({'error': 'Email and password are required fields.'}, status=400)
            
            user = User.objects.get(mail=mail).check_password(password, mail)

            if user.status_code == 200:
                return Response({'Wellcome'}, status=200)
            else:
                return Response({'error': 'Try with valid Email or Password.'}, status=400)
            
        except Exception as e:
            return Response({'error': 'Try with valid Email or Password.'}, status=400)
