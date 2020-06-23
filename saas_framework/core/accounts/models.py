import logging

from django.contrib.auth.models import User
from django.db import models
from saas_framework.core.workspaces.models import Workspace, BaseModel

logger = logging.getLogger(__name__)

class Account(BaseModel):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='+')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    roles = models.CharField(max_length=200)

    class Meta:
        ordering = ['created_at']
        constraints = [
            models.UniqueConstraint(fields= ['workspace','user'], name='unique_account')
        ]
