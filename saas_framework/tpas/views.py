import logging
from saas_framework.tpas.models import AccountThirdPartyApp, ThirdPartyApp
from saas_framework.tpas.serializers import AccountThirdPartyAppSerializer, ThirdPartyAppSerializer
from rest_framework import viewsets

logger = logging.getLogger(__name__)

class ThirdPartyAppViewSet(viewsets.ModelViewSet):
    queryset = ThirdPartyApp.objects.all()
    serializer_class = ThirdPartyAppSerializer
    ordering = 'created_at'

class AccountThirdPartyAppViewSet(viewsets.ModelViewSet):
    queryset = AccountThirdPartyApp.objects.all()
    serializer_class = AccountThirdPartyAppSerializer
    ordering = 'created_at'
