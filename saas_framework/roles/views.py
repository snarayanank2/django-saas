import logging

from rest_framework import viewsets
from saas_framework.roles.models import Role
from saas_framework.roles.serializers import RoleSerializer

logger = logging.getLogger(__name__)

class RoleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    ordering = 'created_at'
