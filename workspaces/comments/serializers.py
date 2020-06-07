import logging

from django.contrib.auth.models import User
from rest_framework import serializers

from workspaces.auth_utils import AuthUtils
from rest_framework.relations import PrimaryKeyRelatedField
from workspaces.workspaces.serializers import WorkspaceSerializerMixin
from workspaces.tags.models import Tag
from workspaces.tags.serializers import TagSerializer
from workspaces.attachments.models import Attachment
from workspaces.comments.models import Comment

logger = logging.getLogger(__name__)

class CommentSerializer(WorkspaceSerializerMixin, serializers.ModelSerializer):
    tag_ids = PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, write_only=True, source='tags')
    tags = TagSerializer(many=True, read_only=True)
    attachment_ids = PrimaryKeyRelatedField(queryset=Attachment.objects.all(), many=True, source='attachments')

    class Meta:
        model = Comment
        fields = ['id', 'message', 'created_at', 'tag_ids', 'tags', 'attachment_ids']
