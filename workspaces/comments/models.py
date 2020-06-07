import logging

from django.db import models
from workspaces.workspaces.models import WorkspaceModelMixin
from workspaces.tags.models import Tag
from workspaces.attachments.models import Attachment
logger = logging.getLogger(__name__)

class Comment(WorkspaceModelMixin):
    message = models.CharField(max_length=1024)
    tags = models.ManyToManyField(Tag)
    attachments = models.ManyToManyField(Attachment)

    def __str__(self):
        return self.id
