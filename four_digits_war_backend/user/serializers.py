# serializers.py
from rest_framework import serializers
from django.db import models

from authentication.models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for reading user data.

    Exposes user id, email, and username fields.
    Used for returning user info in API responses.
    """
    class Meta:
        model = User
        fields = ('id', 'email', 'username')  

class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user data.

    Allows partial updates to 'username' and 'email'.
    Both fields are optional when updating.

    Validates that the email is unique among all users
    except the current instance to prevent duplicates.
    """
    class Meta:
        model = User
        fields = ('username', 'email') 
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': False}
        }

    def validate_email(self, value):
        user = self.instance
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value