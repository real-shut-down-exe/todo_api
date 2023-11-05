from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.user.custom_user_manager import CustomUserManager
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    user_name = None
    email = models.EmailField(_("email address"), unique=True,blank=False,null=False)
    USERNAME_FIELD = "email"
    objects = CustomUserManager()
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
