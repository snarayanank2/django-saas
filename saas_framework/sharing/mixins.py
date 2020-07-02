import logging

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.expressions import Exists, OuterRef
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from saas_framework.sharing.models import Sharing
from saas_framework.workspaces.models import Workspace
from saas_framework.workspaces.serializers import WorkspaceSerializer

logger = logging.getLogger(__name__)

# if you want to associate a model with a workspace, inherit from this modelviewsetmixing
class SharingModelViewSetMixin:
    # need to inherit from perform_create because that has reference to the object
    def perform_create(self, serializer):
        super().perform_create(serializer)
        obj = serializer.instance
        content_type = ContentType.objects.get_for_model(obj)
        workspace = Workspace.objects.get(id=self.request.claim.workspace_id)
        wm = Sharing.objects.create(workspace=workspace, content_type=content_type, object_id=obj.id)
        return obj

    def perform_destroy(self, instance):
        content_type = ContentType.objects.get_for_model(instance)
        wm = Sharing.objects.get(content_type=content_type, object_id=instance.id)
        wm.deleted_at = timezone.now()
        wm.save()

    # by default only returns objects in this workspace
    def get_queryset(self):
        return super().get_queryset().filter(
            Exists(Sharing.objects.filter(object_id=OuterRef('pk'), workspace=self.request.claim.workspace_id, deleted_at__isnull=True)),
        ).order_by('id')
