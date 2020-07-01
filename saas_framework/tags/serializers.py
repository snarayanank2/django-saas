import logging

from rest_framework import serializers
from saas_framework.tags.models import Tag
from rest_framework.relations import PrimaryKeyRelatedField
from saas_framework.workspaces.models import Workspace

logger = logging.getLogger(__name__)

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
