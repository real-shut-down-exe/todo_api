from django.db import models
from apps.user.models import User

class ConnectionRequest(models.Model):
    sender = models.ForeignKey(User, related_name='sent_connection_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_connection_requests', on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver} ({self.created_at})"
