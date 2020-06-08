import logging

from rest_framework import viewsets
from saas_framework.workspaces.models import Workspace
from saas_framework.workspaces.serializers import WorkspaceSerializer

logger = logging.getLogger(__name__)

class WorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    ordering = 'created_at'

