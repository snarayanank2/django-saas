import logging

from django.db import models
from saas_framework.core.accounts.models import Account
from saas_framework.core.tpas.models import ThirdPartyApp
from saas_framework.core.workspaces.models import BaseModel

logger = logging.getLogger(__name__)

class Principal(BaseModel):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='+')
    tpa = models.ForeignKey(ThirdPartyApp, on_delete=models.CASCADE, related_name='+')
    roles = models.CharField(max_length=200)
    class Meta:
        ordering = ['created_at']

