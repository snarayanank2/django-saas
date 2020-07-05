import logging

from rest_framework import serializers

from saas_framework.workspaces.models import Workspace
from rest_framework.relations import PrimaryKeyRelatedField

logger = logging.getLogger(__name__)

class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ['id', 'name']

