import logging

from django.contrib.auth.models import User
from django.db import models
from saas_framework.auth_utils import AuthUtils
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from saas_framework.principals.models import Principal
from saas_framework.workspaces.models import BaseModel, Workspace

logger = logging.getLogger(__name__)

class ClosedSetMember(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='+')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

class ClosedSet(BaseModel):
    members = models.ManyToManyField(ClosedSetMember)
