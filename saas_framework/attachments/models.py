import logging

from django.db import models
from saas_framework.workspaces.models import Workspace

logger = logging.getLogger(__name__)

class Attachment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    file = models.FileField(blank=False, null=False)
    content_type = models.CharField(max_length=100)
    filename = models.CharField(max_length=200)

    def __str__(self):
        return self.file.name
