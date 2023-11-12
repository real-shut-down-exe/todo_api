from rest_framework import viewsets

from apps.user.models import User
from .models import ConnectionRequest
from .serializer import ConnectionRequestSerializer
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status

class ConnectionRequestViewset(viewsets.ModelViewSet):
    queryset = ConnectionRequest.objects.all()
    serializer_class = ConnectionRequestSerializer

    @action(detail=False, methods=['post'])
    def sendARequest(self, request):
        try:

            senderMail = request.data.get('sender', None)
            receiverMail = request.data.get('receiver', None)

            senderData = User.objects.filter(mail=senderMail).first()
            receiverData = User.objects.filter(mail=receiverMail).first()

            if senderData == None or receiverData == None:
                return Response({'error': 'There is no such record in the system.'}, status=status.HTTP_400_BAD_REQUEST)
            else:

                validConnectionRequest = ConnectionRequest.objects.filter(sender = senderData.mail, receiver = receiverData.mail).first()
                if validConnectionRequest:
                    return Response({'error': 'You have already made a request'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    new_user = ConnectionRequest(sender = senderData.mail, receiver = receiverData.mail)
                    new_user.save()
                    return Response({'success': 'request sent'}, status=status.HTTP_200_OK)
                
        except Exception as e:
            return Response({'error': 'Your password or email is incorrect or this mail is in use'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def getAllConnectionByMail(self, request):
        try:
            senderMail = request.data.get('sender', None)
            senderDataList = ConnectionRequest.objects.filter(sender=senderMail)

            date_set = set()
            result_list = []

            if senderDataList == None:
                return Response({'error': 'There is no such record in the system.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                if senderDataList.exists():
                    for senderData in senderDataList:

                        data_tuple = (senderData.sender, senderData.receiver, senderData.is_accepted)                       
                        if data_tuple not in date_set:
                            date_set.add(data_tuple)
                            result_list.append({
                                'sender': senderData.sender,
                                'receiver': senderData.receiver,
                                'is_accepted': senderData.is_accepted,
                            })

            return Response(result_list, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Your password or email is incorrect or this mail is in use'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def fetchSenderAcceptConnections(self, request):
        try:
            senderMail = request.data.get('sender', None)
            senderDataList = ConnectionRequest.objects.filter(sender=senderMail, is_accepted=True)

            result_list = []

            if not senderDataList.exists():
                return Response({'error': 'There is no such record in the system.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                for senderData in senderDataList:
                    result_list.append({
                        'sender': senderData.sender,
                        'receiver': senderData.receiver,
                        'is_accepted': senderData.is_accepted,
                    })

                return Response(result_list, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Your password or email is incorrect or this mail is in use'}, status=status.HTTP_400_BAD_REQUEST)