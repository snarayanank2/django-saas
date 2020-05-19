from rest_framework import serializers
from .models import Workspace, WorkspaceUser, Principal, Comment, Tag
from django.contrib.auth.models import User
import logging
from drf_writable_nested.serializers import WritableNestedModelSerializer

logger = logging.getLogger(__name__)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

class WorkspaceSerializer(serializers.ModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = Workspace
        fields = ['id', 'created_at', 'updated_at', 'name', 'owner']

class WorkspaceUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    workspace = WorkspaceSerializer()

    class Meta:
        model = WorkspaceUser
        fields = ['id', 'created_at', 'updated_at', 'workspace', 'user']

class PrincipalSerializer(serializers.ModelSerializer):
    workspace_user = WorkspaceUserSerializer()

    class Meta:
        model = Principal
        fields = ['id', 'created_at', 'updated_at', 'workspace_user']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class CommentSerializer(WritableNestedModelSerializer):
    created_by = PrincipalSerializer(read_only=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Comment
        fields = ['id', 'message', 'created_at', 'created_by', 'tags']

