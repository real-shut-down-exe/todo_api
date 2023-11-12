from rest_framework import viewsets
from apps.todo.models import Todo
import json
from apps.user.models import User
from .models import ConnectionRequest
from .serializer import ConnectionRequestSerializer, MyCustomSerializer, ReceiverSerializer
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from django.core.serializers import serialize
from django.http import JsonResponse


class ConnectionRequestViewset(viewsets.ModelViewSet):
    queryset = ConnectionRequest.objects.all()
    serializer_class = ConnectionRequestSerializer

    @action(detail=False, methods=["post"])
    def sendARequest(self, request):
        try:
            senderMail = request.data.get("receiver", None)
            receiverMail = request.data.get("sender", None)

            senderData = User.objects.filter(mail=senderMail).first()
            receiverData = User.objects.filter(mail=receiverMail).first()

            if senderData == None or receiverData == None:
                return Response(
                    {"error": "There is no such record in the system."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                validConnectionRequest = ConnectionRequest.objects.filter(
                    sender=senderData.mail, receiver=receiverData.mail
                ).first()

                if validConnectionRequest:
                    return Response(
                        {"error": "You have already made a request"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                else:
                    new_user = ConnectionRequest(
                        sender=senderData.mail, receiver=receiverData.mail, is_accepted=False
                    )
                    new_user.save()
                    return Response(
                        {"success": "request sent"}, status=status.HTTP_200_OK
                    )

        except Exception as e:
            return Response(
                {"error": "Your password or email is incorrect or this mail is in use"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, methods=["post"])
    def getAllConnectionByMail(self, request):
        try:
            senderMail = request.data.get("sender", None)
            senderDataList = ConnectionRequest.objects.filter(sender=senderMail)

            date_set = set()
            result_list = []

            if senderDataList == None:
                return Response(
                    {"error": "There is no such record in the system."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                if senderDataList.exists():
                    for senderData in senderDataList:
                        data_tuple = (
                            senderData.sender,
                            senderData.receiver,
                            senderData.is_accepted,
                        )
                        if data_tuple not in date_set:
                            date_set.add(data_tuple)
                            result_list.append(
                                {
                                    "sender": senderData.sender,
                                    "receiver": senderData.receiver,
                                    "is_accepted": senderData.is_accepted,
                                }
                            )

            return Response(result_list, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "Your password or email is incorrect or this mail is in use"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, methods=["post"])
    def fetchSenderAcceptConnections(self, request):
        try:
            senderMail = request.data.get("sender", None)
            senderDataList = ConnectionRequest.objects.filter(
                sender=senderMail, is_accepted=True
            )

            result_list = []

            if not senderDataList.exists():
                return Response(
                    {"error": "There is no such record in the system."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                for senderData in senderDataList:
                    result_list.append(
                        {
                            "sender": senderData.sender,
                            "receiver": senderData.receiver,
                            "is_accepted": senderData.is_accepted,
                        }
                    )

                return Response(result_list, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "Your password or email is incorrect or this mail is in use"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, methods=["post"])
    def HaveAnAcceptConnections(self, request):
        try:
            senderMail = request.data.get("sender", None)
            senderDataList = ConnectionRequest.objects.filter(
                sender=senderMail, is_accepted=True
            )

            result_list = []

            if not senderDataList.exists():
                return Response(False, status=status.HTTP_200_OK)
            else:
                return Response(True, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "Your password or email is incorrect or this mail is in use"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @swagger_auto_schema(request_body=ReceiverSerializer)
    @action(detail=False, methods=["post"])
    def HaveAnyRequest(self, request):
        try:
            receiverMail = request.data.get("receiver", None)
            receiverDataList = ConnectionRequest.objects.filter(
                receiver=receiverMail, is_accepted=False
            )

            result_list = []

            if not receiverDataList.exists():
                return Response(
                    status=status.HTTP_204_NO_CONTENT,
                )
            else:
                for receiverData in receiverDataList:
                    sender_exists = any(item["sender"] == receiverData.sender for item in result_list)

                    if not sender_exists:
                        result_list.append({
                            "sender": receiverData.sender,
                            "pk": receiverData.pk
                            })

                return Response(result_list, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "Your password or email is incorrect or this mail is in use"},
                status=status.HTTP_200_OK,
            )

    @swagger_auto_schema(request_body=MyCustomSerializer)
    @action(detail=False, methods=["post"])
    def fetchAcceptConnectionsTodos(self, request):
        try:
            senderMail = request.data.get("sender", None)
            senderDataList = ConnectionRequest.objects.filter(
                sender=senderMail, is_accepted=True
            )

            receiver_result_dict = []  # Değişiklik burada

            if not senderDataList.exists():
                return Response(
                    {"error": "There is no such record in the system."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                for senderData in senderDataList:
                    receiver_email = senderData.receiver

                    receiver_user_data = serialize(
                        "json", [User.objects.get(mail=receiver_email)]
                    )
                    receiver_user = json.loads(receiver_user_data)[0]["pk"]
                    receiver_todos = Todo.objects.filter(created_by=receiver_user)

                    response_data = {
                        "receiver": senderData.receiver,
                        "receiver_id": receiver_user,
                        "todos": [
                            {
                                "title": todo.title,
                                "created_by": todo.created_by.pk,
                                "created_at": todo.created_at,
                                "is_deleted": todo.is_deleted,
                            }
                            for todo in receiver_todos
                        ],
                    }

                    # Burada listeye eklemek yerine sözlüğe anahtar olarak ekliyoruz
                    receiver_result_dict.append(response_data)

                return Response(
                    receiver_result_dict,
                    status=status.HTTP_200_OK,
                )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


    @action(detail=False, methods=["post"])
    def updateConnectionRequest(self, request):
        try:
            connection_request_pk = request.data.get("pk")

            connection_request = ConnectionRequest.objects.get(pk=connection_request_pk)

            connection_request.is_accepted = request.data.get("is_accepted", connection_request.is_accepted)

            connection_request.save()

            return Response({"success": "ConnectionRequest updated successfully"})

        except ConnectionRequest.DoesNotExist:
            return Response(
                {"error": "ConnectionRequest with the provided pk does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
    @action(detail=False, methods=["post"])
    def deleteConnectionRequest(self, request):
        try:
            connection_request_pk = request.data.get("pk")
            connection_request = ConnectionRequest.objects.get(pk=connection_request_pk)
            connection_request.delete()

            return Response({"success": "ConnectionRequest deleted successfully"})

        except ConnectionRequest.DoesNotExist:
            return Response(
                {"error": "ConnectionRequest with the provided pk does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
    