import logging

from django.contrib.auth.models import User
from rest_framework import serializers

from rest_framework.relations import PrimaryKeyRelatedField
from saas_framework.tags.models import Tag
from saas_framework.tags.serializers import TagSerializer
from saas_framework.attachments.models import Attachment
from saas_framework.comments.models import Comment
from saas_framework.core.workspaces.models import Workspace

logger = logging.getLogger(__name__)

class CommentSerializer(serializers.ModelSerializer):
    tag_ids = PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, write_only=True, source='tags')
    tags = TagSerializer(many=True, read_only=True)
    attachment_ids = PrimaryKeyRelatedField(queryset=Attachment.objects.all(), many=True, source='attachments')

    class Meta:
        model = Comment
        fields = ['id', 'message', 'created_at', 'tag_ids', 'tags', 'attachment_ids']
