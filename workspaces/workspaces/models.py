import logging

from django.contrib.auth.models import User
from django.db import models
from workspaces.auth_utils import AuthUtils

logger = logging.getLogger(__name__)

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Workspace(BaseModel):
    name = models.CharField(max_length=200)

