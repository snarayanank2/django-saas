import logging


from rest_framework import viewsets
from saas_framework.tags.models import Tag
from saas_framework.tags.serializers import TagSerializer

logger = logging.getLogger(__name__)

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    ordering = 'created_at'
