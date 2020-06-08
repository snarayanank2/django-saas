import logging

from django.db import models
from workspaces.accounts.models import Account
from workspaces.tpas.models import ThirdPartyApp
from workspaces.workspaces.models import BaseModel

logger = logging.getLogger(__name__)

class Principal(BaseModel):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='+')
    tpa = models.ForeignKey(ThirdPartyApp, on_delete=models.CASCADE, related_name='+')
    roles = models.CharField(max_length=200)
    class Meta:
        ordering = ['created_at']

