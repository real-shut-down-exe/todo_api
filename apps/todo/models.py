from django.db import models

from apps.user.models import User

class Todo(models.Model):
    STATUS_CHOICES = [
        ("To Do", "To Do"),
        ("In Progress", "In Progress"),
        ("Done", "Done"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    status = models.CharField(
        max_length = 20,
        choices = STATUS_CHOICES,
        default="To Do",
    )

    def __str__(self):
        return self.title
