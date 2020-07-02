import logging

from django.db import models
from django.contrib.auth.models import User

from saas_framework.workspaces.models import Workspace

logger = logging.getLogger(__name__)

class ThirdPartyApp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    name = models.TextField()
    secret = models.TextField()
    description = models.TextField()
    enabled = models.BooleanField()
    redirect_uris = models.TextField()

    class Meta:
        ordering = ['id']

class ThirdPartyAppInstall(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='+')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    tpa = models.ForeignKey(ThirdPartyApp, on_delete=models.CASCADE, related_name='+')
    roles = models.TextField()
    class Meta:
        ordering = ['id']

