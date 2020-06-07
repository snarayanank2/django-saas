import logging

from django.contrib.auth.models import User
from django.db import models
from workspaces.auth_utils import AuthUtils

logger = logging.getLogger(__name__)

# TODO: convert this to a mixin
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Workspace(BaseModel):
    name = models.CharField(max_length=200)
    
# This is the important class that others should inherit from
# TODO: mixing shouldn't inherit from BaseModel
class WorkspaceModelMixin(BaseModel):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='+')

    class Meta:
        abstract = True
