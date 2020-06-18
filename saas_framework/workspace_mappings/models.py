import logging

from django.contrib.auth.models import User
from django.db import models
from saas_framework.auth_utils import AuthUtils
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from saas_framework.principals.models import Principal
from saas_framework.workspaces.models import BaseModel, Workspace

logger = logging.getLogger(__name__)

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

class WorkspaceMapping(BaseModel):
    # overload objectmanager to only return things that have not been deleted
    objects = SoftDeleteManager()
    all_objects = models.Manager()

    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='+')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='+')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_by = models.ForeignKey(Principal, on_delete=models.CASCADE, related_name='+', null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

