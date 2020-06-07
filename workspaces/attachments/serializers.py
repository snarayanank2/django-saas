import logging

from rest_framework import serializers

from workspaces.attachments.models import Attachment
from workspaces.workspaces.serializers import WorkspaceSerializerMixin

logger = logging.getLogger(__name__)

class AttachmentSerializer(WorkspaceSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['id', 'file', 'content_type', 'filename']
