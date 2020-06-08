import logging

from django.db import models
from saas_framework.workspaces.models import Workspace, BaseModel

logger = logging.getLogger(__name__)

class Attachment(BaseModel):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='+')
    file = models.FileField(blank=False, null=False)
    content_type = models.CharField(max_length=100)
    filename = models.CharField(max_length=200)

    def __str__(self):
        return self.file.name
