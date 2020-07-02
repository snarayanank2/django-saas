import logging

from django.contrib.auth.models import User
from django.db import models
from saas_framework.workspaces.models import BaseModel, Workspace

logger = logging.getLogger(__name__)

class Team(BaseModel):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='+')
    hidden = models.BooleanField(default=False)
    name = models.TextField(blank=True, null=True)
    users = models.ManyToManyField(User)
