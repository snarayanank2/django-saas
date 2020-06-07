import logging
from rest_framework import viewsets
from workspaces.principals.models import Principal
from workspaces.principals.serializers import PrincipalSerializer

logger = logging.getLogger(__name__)

class PrincipalViewSet(viewsets.ModelViewSet):
    queryset = Principal.objects.all()
    serializer_class = PrincipalSerializer
    ordering = 'created_at'
