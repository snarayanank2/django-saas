import logging
from saas_framework.tpas.models import ThirdPartyApp
from saas_framework.tpas.serializers import ThirdPartyAppSerializer
from rest_framework import viewsets

logger = logging.getLogger(__name__)

class ThirdPartyAppViewSet(viewsets.ModelViewSet):
    queryset = ThirdPartyApp.objects.all()
    serializer_class = ThirdPartyAppSerializer
    ordering = 'created_at'

