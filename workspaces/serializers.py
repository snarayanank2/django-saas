import logging

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import (Attachment, Comment, Principal, Tag, Workspace,
                     WorkspaceUser, WorkspaceSchedule)
from django_q.models import Schedule, Task
from rest_framework.relations import PrimaryKeyRelatedField

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

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['name', 'func', 'args', 'kwargs', 'schedule_type', 'repeats', 'next_run']

class WorkspaceScheduleSerializer(serializers.ModelSerializer):
    workspace = WorkspaceSerializer()
    schedule = ScheduleSerializer()

    class Meta:
        model = WorkspaceSchedule
        fields = ['created_at', 'id', 'workspace', 'schedule']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['id', 'file', 'content_type', 'filename']

class CommentSerializer(serializers.ModelSerializer):
    created_by = PrincipalSerializer(read_only=True)
    tag_ids = PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, write_only=True, source='tags')
    tags = TagSerializer(many=True, read_only=True)
    attachment_ids = PrimaryKeyRelatedField(queryset=Attachment.objects.all(), many=True, source='attachments')

    class Meta:
        model = Comment
        fields = ['id', 'message', 'created_at', 'created_by', 'tag_ids', 'tags', 'attachment_ids']
