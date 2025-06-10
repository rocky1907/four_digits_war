# serializers.py
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import User
import logging

logger = logging.getLogger('all_api')


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    - Validates password using Django's built-in validators.
    - Creates a new user instance securely with hashed password.
    - Logs relevant creation steps and errors for monitoring and troubleshooting.
    """
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password')

    def create(self, validated_data):
        # Log user creation attempt excluding sensitive password field
        logger.debug("Creating user with data: %s", {k: v for k, v in validated_data.items() if k != 'password'})
        try:
            user = User.objects.create_user(**validated_data)
            logger.info("User created in DB: %s", user.email)
            return user
        except Exception as err:
            logger.error("Failed to create user: %s", str(err))
            # Raise validation error to inform the API client about failure
            raise serializers.ValidationError("Could not register user.")