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
        fields = ['id', 'workspace', 'user', 'role']

class PrincipalSerializer(serializers.ModelSerializer):
    account = AccountSerializer(read_only=True)
    client_application = ClientApplicationSerializer(read_only=True)

    class Meta:
        model = Principal
        fields = ['id', 'account', 'client_application']

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['id', 'name', 'func', 'args', 'kwargs', 'schedule_type', 'repeats', 'next_run']

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
