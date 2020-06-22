import logging

from rest_framework import viewsets
from saas_framework.core.workspaces.models import Workspace
from saas_framework.core.workspaces.serializers import WorkspaceSerializer
from saas_framework.core.auth_utils import AuthUtils
from django.contrib.contenttypes.models import ContentType
from django.db.models.expressions import Exists, OuterRef
from saas_framework.core.principals.models import Principal
#from django.utils import timezone

logger = logging.getLogger(__name__)

class WorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    ordering = 'created_at'

