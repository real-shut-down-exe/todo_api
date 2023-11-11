from django.db import models
from apps.user.models import User

class ConnectionRequest(models.Model):
    sender = models.CharField(max_length=250)
    receiver = models.CharField(max_length=250)
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver} ({self.created_at})"
