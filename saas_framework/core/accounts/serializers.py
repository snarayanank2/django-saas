import logging

from django.contrib.auth.models import User
from rest_framework import serializers

from rest_framework.relations import PrimaryKeyRelatedField
from saas_framework.core.users.serializers import UserSerializer
from saas_framework.core.workspaces.serializers import WorkspaceSerializer
from saas_framework.core.accounts.models import Account
logger = logging.getLogger(__name__)


class AccountSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    workspace = WorkspaceSerializer()

    class Meta:
        model = Account
        fields = ['id', 'workspace', 'user', 'roles']

