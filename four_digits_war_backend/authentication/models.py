# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=False, blank=True, null=True)

    USERNAME_FIELD = 'username'  
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
