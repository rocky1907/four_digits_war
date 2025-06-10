# views.py
from rest_framework import generics, permissions
from .serializers import RegisterSerializer
from .models import User
import logging

logger = logging.getLogger('all_api')

class RegisterView(generics.CreateAPIView):
    """
    Handles user registration.

    Logs registration attempts, successes, and errors for monitoring.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        logger.info("New user registration attempt: %s", request.data.get('email'))
        try:
            response = super().create(request, *args, **kwargs)
            logger.info("User registered successfully: %s", response.data.get('email'))
            return response
        except Exception as err:
            logger.error("Error registering user: %s", str(err))
            raise
