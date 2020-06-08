import logging

from rest_framework import serializers

from saas_framework.attachments.models import Attachment
from rest_framework.relations import PrimaryKeyRelatedField
from saas_framework.workspaces.models import Workspace

logger = logging.getLogger(__name__)

class AttachmentSerializer(serializers.ModelSerializer):
    workspace_id = PrimaryKeyRelatedField(queryset=Workspace.objects.all(), source='workspace')

    class Meta:
        model = Attachment
        fields = ['id', 'file', 'content_type', 'filename', 'workspace_id']
