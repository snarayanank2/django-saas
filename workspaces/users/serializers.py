import logging

from django.contrib.auth.models import User
from rest_framework import serializers

logger = logging.getLogger(__name__)

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'username']

