import logging

from rest_framework import serializers
from saas_framework.tpas.models import ThirdPartyApp
from rest_framework.relations import PrimaryKeyRelatedField
from saas_framework.workspaces.models import Workspace
from saas_framework.workspaces.serializers import WorkspaceSerializer
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from saas_framework.users.serializers import UserSerializer

logger = logging.getLogger(__name__)

class ThirdPartyAppSerializer(serializers.ModelSerializer):
    creator_id = PrimaryKeyRelatedField(queryset=User.objects.all(), source='creator', write_only=True)
    creator = UserSerializer(read_only=True)
    secret = serializers.CharField(write_only=True)

    def create(self, validated_data):
        validated_data['secret'] = make_password(validated_data['secret'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('secret', None)
        return super.update(instance, validated_data)

    class Meta:
        model = ThirdPartyApp
        fields = ['id', 'creator_id', 'creator', 'name', 'secret', 'description', 'enabled', 'redirect_uris']
    

class ThirdPartyAppInstallSerializer(serializers.ModelSerializer):
    workspace_id = PrimaryKeyRelatedField(queryset=Workspace.objects.all(), source='workspace', write_only=True)
    workspace = WorkspaceSerializer(read_only=True)
    user_id = PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)
    user = UserSerializer(read_only=True)
    tpa_id = PrimaryKeyRelatedField(queryset=ThirdPartyApp.objects.all(), source='tpa', write_only=True)
    tpa = ThirdPartyAppSerializer(read_only=True)

    class Meta:
        model = ThirdPartyApp
        fields = ['id', 'workspace_id', 'workspace', 'user_id', 'user', 'tpa_id', 'tpa', 'roles']
