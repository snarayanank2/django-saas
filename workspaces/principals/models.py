import logging

from django.db import models
from workspaces.accounts.models import Account
from workspaces.tpas.models import ClientApplication
from workspaces.workspaces.models import BaseModel

logger = logging.getLogger(__name__)

# TODO - extend workspacemodelmixin
class Principal(BaseModel):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='+')
    client_application = models.ForeignKey(ClientApplication, on_delete=models.CASCADE, related_name='+')
    roles = models.CharField(max_length=200)
    class Meta:
        ordering = ['created_at']

