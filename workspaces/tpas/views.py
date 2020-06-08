import logging
from workspaces.tpas.models import ThirdPartyApp
from workspaces.tpas.serializers import ThirdPartyAppSerializer
from rest_framework import viewsets

logger = logging.getLogger(__name__)

class ThirdPartyAppViewSet(viewsets.ModelViewSet):
    queryset = ThirdPartyApp.objects.all()
    serializer_class = ThirdPartyAppSerializer
    ordering = 'created_at'

