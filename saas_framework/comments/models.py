import logging

from django.db import models
from saas_framework.tags.models import Tag
from saas_framework.attachments.models import Attachment
from saas_framework.workspaces.models import Workspace, BaseModel
logger = logging.getLogger(__name__)

class Comment(BaseModel):
    message = models.CharField(max_length=1024)
    tags = models.ManyToManyField(Tag)
    attachments = models.ManyToManyField(Attachment)

    def __str__(self):
        return self.id
