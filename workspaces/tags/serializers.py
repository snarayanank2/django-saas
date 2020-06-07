import logging

from rest_framework import serializers
from workspaces.tags.models import Tag
from workspaces.workspaces.serializers import WorkspaceSerializerMixin

logger = logging.getLogger(__name__)

class TagSerializer(WorkspaceSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
