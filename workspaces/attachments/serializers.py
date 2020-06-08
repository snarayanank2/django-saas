import logging

from rest_framework import serializers

from workspaces.attachments.models import Attachment
from rest_framework.relations import PrimaryKeyRelatedField
from workspaces.workspaces.models import Workspace

logger = logging.getLogger(__name__)

class AttachmentSerializer(serializers.ModelSerializer):
    workspace_id = PrimaryKeyRelatedField(queryset=Workspace.objects.all(), source='workspace')

    class Meta:
        model = Attachment
        fields = ['id', 'file', 'content_type', 'filename', 'workspace_id']
