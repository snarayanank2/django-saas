import logging

from django.db import models
from workspaces.workspaces.models import WorkspaceModelMixin

logger = logging.getLogger(__name__)

class Attachment(WorkspaceModelMixin):
    file = models.FileField(blank=False, null=False)
    content_type = models.CharField(max_length=100)
    filename = models.CharField(max_length=200)

    def __str__(self):
        return self.file.name
