import logging

from django.contrib.auth.models import User
from django.db import models
from saas_framework.workspaces.models import Workspace

logger = logging.getLogger(__name__)

class Role(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='+')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    scope = models.CharField(max_length=200)

    class Meta:
        ordering = ['created_at']
        constraints = [
            models.UniqueConstraint(fields= ['workspace','user'], name='unique_role')
        ]
