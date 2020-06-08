import logging

from django.db import models
from django.contrib.auth.models import User

from saas_framework.workspaces.models import BaseModel, Workspace
from saas_framework.accounts.models import Account
from django.contrib.auth.hashers import make_password

logger = logging.getLogger(__name__)

class ThirdPartyApp(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    name = models.TextField()
    secret = models.TextField()
    description = models.TextField()
    enabled = models.BooleanField()
    redirect_uris = models.TextField()

    class Meta:
        ordering = ['id']

class AccountThirdPartyApp(BaseModel):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='+')
    tpa = models.ForeignKey(ThirdPartyApp, on_delete=models.CASCADE, related_name='+')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='+')
    roles = models.CharField(max_length=200)
    class Meta:
        ordering = ['id']
