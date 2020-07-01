import logging

from django.contrib.auth.hashers import make_password
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from saas_framework.accounts.models import Account
from saas_framework.auth.claim import Claim
from saas_framework.principals.models import Principal
from saas_framework.tpas.models import AccountThirdPartyApp, ThirdPartyApp
from saas_framework.tpas.serializers import (
    AccountThirdPartyAppSerializer, ThirdPartyAppSerializer)
from saas_framework.workspaces.models import Workspace

logger = logging.getLogger(__name__)

class ThirdPartyAppViewSet(viewsets.ModelViewSet):
    queryset = ThirdPartyApp.objects.all()
    serializer_class = ThirdPartyAppSerializer
    ordering = 'created_at'

class AccountThirdPartyAppViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AccountThirdPartyApp.objects.all()
    serializer_class = AccountThirdPartyAppSerializer
    ordering = 'created_at'
