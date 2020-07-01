import logging

from rest_framework import serializers
from saas_framework.tpas.models import ThirdPartyApp
from saas_framework.accounts.serializers import AccountSerializer
from rest_framework.relations import PrimaryKeyRelatedField
from saas_framework.accounts.models import Account
from saas_framework.workspaces.models import Workspace
from saas_framework.workspaces.serializers import WorkspaceSerializer
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from saas_framework.users.serializers import UserSerializer

logger = logging.getLogger(__name__)

class ThirdPartyAppSerializer(serializers.ModelSerializer):
    user_id = PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)
    user = UserSerializer(read_only=True)
    secret = serializers.CharField(write_only=True)

    def create(self, validated_data):
        validated_data['secret'] = make_password(validated_data['secret'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('secret', None)
        return super.update(instance, validated_data)

    class Meta:
        model = ThirdPartyApp
        fields = ['id', 'user_id', 'user', 'name', 'secret', 'description', 'enabled', 'redirect_uris']
    

class AccountThirdPartyAppSerializer(serializers.ModelSerializer):
    workspace_id = PrimaryKeyRelatedField(queryset=Workspace.objects.all(), source='workspace', write_only=True)
    workspace = WorkspaceSerializer(read_only=True)
    account_id = PrimaryKeyRelatedField(queryset=Account.objects.all(), source='account', write_only=True)
    account = AccountSerializer(read_only=True)
    tpa_id = PrimaryKeyRelatedField(queryset=ThirdPartyApp.objects.all(), source='tpa', write_only=True)
    tpa = ThirdPartyAppSerializer(read_only=True)

    class Meta:
        model = ThirdPartyApp
        fields = ['id', 'workspace_id', 'workspace', 'account_id', 'account', 'tpa_id', 'tpa', 'roles']
