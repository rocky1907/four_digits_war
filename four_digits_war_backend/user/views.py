from rest_framework import generics, permissions
from authentication.models import User
from .serializers import UserSerializer, UserUpdateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
import logging

logger = logging.getLogger('all_api')


class UserListView(generics.ListAPIView):
    """
    List all users – only for authenticated users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        logger.info(f"User {request.user.email} requested the user list")
        return super().list(request, *args, **kwargs)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve/update/delete a user by ID – requires authentication.
    """
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserSerializer

    def retrieve(self, request, *args, **kwargs):
        logger.info(f"User {request.user.email} retrieved details for user id {kwargs.get('pk')}")
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.info(f"User {request.user.email} is updating user id {kwargs.get('pk')} with data {request.data}")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logger.warning(f"User {request.user.email} deleted user id {kwargs.get('pk')}")
        return super().destroy(request, *args, **kwargs)


class UserMeView(APIView):
    """
    Retrieve the currently authenticated user's own profile.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        logger.info(f"User {request.user.email} requested their own profile")
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
