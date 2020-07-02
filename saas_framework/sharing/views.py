import logging

from rest_framework import viewsets
from saas_framework.sharing.models import Sharing
from saas_framework.sharing.serializers import SharingSerializer

logger = logging.getLogger(__name__)

class SharingViewSet(viewsets.ModelViewSet):
    queryset = Sharing.objects.all()
    serializer_class = SharingSerializer
    ordering = 'created_at'
