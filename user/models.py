from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=9, null=True, blank=True)

    USERNAME_FIELD = 'phone'