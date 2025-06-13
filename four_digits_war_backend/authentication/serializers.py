# serializers.py
from rest_framework import serializers
from .models import User

class QuickLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)

    def create(self, validated_data):
        username = validated_data['username']
        user, _ = User.objects.get_or_create(username=username)
        return user
