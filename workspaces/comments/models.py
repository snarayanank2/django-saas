import logging

from django.db import models
from workspaces.tags.models import Tag
from workspaces.attachments.models import Attachment
from workspaces.workspaces.models import Workspace, BaseModel
logger = logging.getLogger(__name__)

class Comment(BaseModel):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='+')
    message = models.CharField(max_length=1024)
    tags = models.ManyToManyField(Tag)
    attachments = models.ManyToManyField(Attachment)

    def __str__(self):
        return self.id
