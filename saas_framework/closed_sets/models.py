import logging

from django.contrib.auth.models import User
from django.db import models
from saas_framework.auth_utils import AuthUtils
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from saas_framework.principals.models import Principal
from saas_framework.workspaces.models import BaseModel, Workspace

logger = logging.getLogger(__name__)

class ClosedSet(BaseModel):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class ClosedSetMembership:
    closed_set = models.ForeignKey(ClosedSet, on_delete=models.CASCADE, related_name='+')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='+')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
