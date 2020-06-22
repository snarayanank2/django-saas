import logging

from rest_framework import viewsets
from saas_framework.workspaces.models import Workspace
from saas_framework.workspace_membership.models import WorkspaceMembership
from saas_framework.workspaces.serializers import WorkspaceSerializer
from saas_framework.auth_utils import AuthUtils
from django.contrib.contenttypes.models import ContentType
from django.db.models.expressions import Exists, OuterRef
from saas_framework.principals.models import Principal
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound

logger = logging.getLogger(__name__)

# if you want to associate a model with a workspace, inherit from this modelviewsetmixing
class WorkspaceMembershipModelViewSetMixin:
    # need to inherit from perform_create because that has reference to the object
    def perform_create(self, serializer):
        super().perform_create(serializer)
        obj = serializer.instance
        content_type = ContentType.objects.get_for_model(obj)
        workspace = Workspace.objects.get(id=AuthUtils.get_current_workspace_id())
        principal = Principal.objects.get(id=AuthUtils.get_current_principal_id())
        wm = WorkspaceMembership.objects.create(workspace=workspace, content_type=content_type, object_id=obj.id, created_by=principal)
        return obj

    def perform_destroy(self, instance):
        content_type = ContentType.objects.get_for_model(instance)
        try:
            wm = WorkspaceMembership.objects.get(content_type=content_type, object_id=instance.id)
        except ObjectDoesNotExist:
            raise NotFound()
        wm.deleted_at = timezone.now()
        wm.save()


    # by default only returns objects in this workspace
    def get_queryset(self):
        return super().get_queryset().filter(
            Exists(WorkspaceMembership.objects.filter(object_id=OuterRef('pk'), workspace=AuthUtils.get_current_workspace_id())),
        ).order_by('id')

