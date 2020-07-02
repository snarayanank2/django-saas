import logging

from rest_framework import serializers

from saas_framework.teams.models import Team
from django.contrib.auth.models import User
from rest_framework.relations import PrimaryKeyRelatedField
from saas_framework.users.serializers import UserSerializer

logger = logging.getLogger(__name__)

class TeamSerializer(serializers.ModelSerializer):
    user_ids = PrimaryKeyRelatedField(queryset=User.objects.all(), many=True, write_only=True, source='users')
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'hidden', 'name', 'user_ids', 'users']

