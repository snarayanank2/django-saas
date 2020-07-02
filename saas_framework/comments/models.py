import logging

from django.db import models
from saas_framework.tags.models import Tag
from saas_framework.attachments.models import Attachment
from saas_framework.workspaces.models import Workspace
logger = logging.getLogger(__name__)

class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    message = models.CharField(max_length=1024)
    tags = models.ManyToManyField(Tag)
    attachments = models.ManyToManyField(Attachment)

    def __str__(self):
        return self.id
