import logging

from rest_framework import viewsets
from saas_framework.workspaces.models import Workspace, WorkspaceMapping
from saas_framework.workspaces.serializers import WorkspaceSerializer
from saas_framework.auth_utils import AuthUtils
from django.contrib.contenttypes.models import ContentType
from django.db.models.expressions import Exists, OuterRef

logger = logging.getLogger(__name__)

class WorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    ordering = 'created_at'

# if you want to associate a model with a workspace, inherit from this modelviewsetmixing
class WorkspaceMappingModelViewSetMixin:
    # need to inherit from perform_create because that has reference to the object
    def perform_create(self, serializer):
        workspace = Workspace.objects.get(id=AuthUtils.get_current_workspace_id())
        super().perform_create(serializer)
        obj = serializer.instance
        content_type = ContentType.objects.get_for_model(obj)
        wm = WorkspaceMapping.objects.create(workspace=workspace, content_type=content_type, object_id=obj.id)
        return obj

    def get_queryset(self):
        return super().get_queryset().filter(
            Exists(WorkspaceMapping.objects.filter(object_id=OuterRef('pk'), workspace=AuthUtils.get_current_workspace_id()))
        ).order_by('id')

