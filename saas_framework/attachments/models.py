import logging

from django.db import models
from saas_framework.core.workspaces.models import Workspace, BaseModel

logger = logging.getLogger(__name__)

class Attachment(BaseModel):
    file = models.FileField(blank=False, null=False)
    content_type = models.CharField(max_length=100)
    filename = models.CharField(max_length=200)

    def __str__(self):
        return self.file.name
