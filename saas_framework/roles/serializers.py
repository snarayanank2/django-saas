import logging

from django.contrib.auth.models import User
from rest_framework import serializers

from saas_framework.roles.models import Role
from saas_framework.workspaces.models import Workspace
from saas_framework.users.serializers import UserSerializer
from saas_framework.workspaces.serializers import WorkspaceSerializer

logger = logging.getLogger(__name__)

class RoleSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    workspace = WorkspaceSerializer()

    class Meta:
        model = Role
        fields = ['id', 'workspace', 'user', 'roles']

