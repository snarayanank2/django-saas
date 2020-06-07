import logging

from django.db import models
from workspaces.workspaces.models import WorkspaceModelMixin

logger = logging.getLogger(__name__)

class Tag(WorkspaceModelMixin):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
