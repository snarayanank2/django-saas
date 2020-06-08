import logging

from rest_framework import serializers
from workspaces.tags.models import Tag
from rest_framework.relations import PrimaryKeyRelatedField
from workspaces.workspaces.models import Workspace

logger = logging.getLogger(__name__)

class TagSerializer(serializers.ModelSerializer):
    workspace_id = PrimaryKeyRelatedField(queryset=Workspace.objects.all(), source='workspace')

    class Meta:
        model = Tag
        fields = ['id', 'name', 'workspace_id']