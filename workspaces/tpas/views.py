import logging
from workspaces.tpas.models import ClientApplication
from workspaces.tpas.serializers import ClientApplicationSerializer
from rest_framework import viewsets

logger = logging.getLogger(__name__)

class ClientApplicationViewSet(viewsets.ModelViewSet):
    queryset = ClientApplication.objects.all()
    serializer_class = ClientApplicationSerializer
    ordering = 'created_at'

