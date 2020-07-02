import logging

from django.db import models
from saas_framework.workspaces.models import Workspace

logger = logging.getLogger(__name__)

class Tag(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
