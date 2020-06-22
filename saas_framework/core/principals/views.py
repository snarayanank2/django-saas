import logging
from rest_framework import viewsets
from saas_framework.core.principals.models import Principal
from saas_framework.core.principals.serializers import PrincipalSerializer

logger = logging.getLogger(__name__)

class PrincipalViewSet(viewsets.ModelViewSet):
    queryset = Principal.objects.all()
    serializer_class = PrincipalSerializer
    ordering = 'created_at'