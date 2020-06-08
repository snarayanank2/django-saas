import logging

from django.db import models
from workspaces.workspaces.models import BaseModel

logger = logging.getLogger(__name__)

class ThirdPartyApp(BaseModel):
    name = models.CharField(max_length=200)
    class Meta:
        ordering = ['id']
