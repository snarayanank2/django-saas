import logging

from django.db import models
from saas_framework.core.workspaces.models import Workspace, BaseModel

logger = logging.getLogger(__name__)

class Tag(BaseModel):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
