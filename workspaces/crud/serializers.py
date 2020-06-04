import logging

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import (Attachment, Comment, Principal, Tag, Workspace,
                     Account, WorkspaceSchedule, ClientApplication)
from django_q.models import Schedule, Task
from rest_framework.relations import PrimaryKeyRelatedField

logger = logging.getLogger(__name__)

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'username']

class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ['id', 'name']

class ClientApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientApplication
        fields = ['id', 'name']

class AccountSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    workspace = WorkspaceSerializer()

    class Meta:
        model = Account
        fields = ['id', 'workspace', 'user', 'roles']

class PrincipalSerializer(serializers.ModelSerializer):
    account = AccountSerializer()
    client_application = ClientApplicationSerializer()

    class Meta:
        model = Principal
        fields = ['id', 'account', 'client_application', 'roles']

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['id', 'name', 'func', 'args', 'kwargs', 'schedule_type', 'repeats', 'next_run']

class TagSerializer(serializers.ModelSerializer):
    workspace_id = PrimaryKeyRelatedField(queryset=Workspace.objects.all(), source='workspace', allow_null=True)
    class Meta:
        model = Tag
        fields = ['id', 'name', 'workspace_id']

class AttachmentSerializer(serializers.ModelSerializer):
    workspace_id = PrimaryKeyRelatedField(queryset=Workspace.objects.all(), source='workspace', allow_null=True)
    class Meta:
        model = Attachment
        fields = ['id', 'file', 'content_type', 'filename', 'workspace_id']

class CommentSerializer(serializers.ModelSerializer):
    workspace_id = PrimaryKeyRelatedField(queryset=Workspace.objects.all(), source='workspace', allow_null=True)
    tag_ids = PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, write_only=True, source='tags')
    tags = TagSerializer(many=True, read_only=True)
    attachment_ids = PrimaryKeyRelatedField(queryset=Attachment.objects.all(), many=True, source='attachments')

    class Meta:
        model = Comment
        fields = ['id', 'message', 'created_at', 'tag_ids', 'tags', 'attachment_ids', 'workspace_id']
