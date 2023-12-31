from django.db import models
from rest_framework.response import Response

class User(models.Model):
    USER_TYPE = [
        ("Admin", "Admin"),
        ("User", "User"),
    ]

    mail = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE,
        default="User",
    )

    def __str__(self):
        return self.mail

    def get_created_by_mail(self):
        if self.created_by:
            return self.created_by.mail
        return None
    
    def check_password(self, password, mail):
        if self.password == password and self.mail == mail:
            # return Response(status=200)
            return Response(self, status=200)
        
        else:
            return Response(status=400)