import logging

from rest_framework import viewsets

from saas_framework.tpas.models import (ThirdPartyAppInstall, ThirdPartyApp)
from saas_framework.tpas.serializers import (
    ThirdPartyAppInstallSerializer, ThirdPartyAppSerializer)

logger = logging.getLogger(__name__)

class ThirdPartyAppViewSet(viewsets.ModelViewSet):
    queryset = ThirdPartyApp.objects.all()
    serializer_class = ThirdPartyAppSerializer
    ordering = 'created_at'

class ThirdPartyAppInstallViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ThirdPartyAppInstall.objects.all()
    serializer_class = ThirdPartyAppInstallSerializer
    ordering = 'created_at'

    # TODO: allow deletion, but not creation via view
