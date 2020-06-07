import logging

from django.contrib.auth.models import User
from django.db import models
from workspaces.workspaces.models import WorkspaceModelMixin
from workspaces.auth_utils import AuthUtils

logger = logging.getLogger(__name__)

class Account(WorkspaceModelMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    roles = models.CharField(max_length=200)

    class Meta:
        ordering = ['created_at']
        constraints = [
            models.UniqueConstraint(fields= ['workspace','user'], name='unique_account')
        ]
