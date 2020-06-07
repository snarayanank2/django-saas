import logging

from rest_framework import viewsets
from workspaces.workspaces.models import Workspace
from workspaces.workspaces.serializers import WorkspaceSerializer

logger = logging.getLogger(__name__)

class WorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    ordering = 'created_at'

