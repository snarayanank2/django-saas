import logging

from rest_framework import serializers

from workspaces.workspaces.models import Workspace
from rest_framework.relations import PrimaryKeyRelatedField

logger = logging.getLogger(__name__)

class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ['id', 'name']

# Serializers for workspace objects should inherit from this
class WorkspaceSerializerMixin:
    workspace_id = PrimaryKeyRelatedField(queryset=Workspace.objects.all(), source='workspace')
    class Meta:
        abstract = True

