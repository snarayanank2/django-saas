import logging


from rest_framework import viewsets
from workspaces.tags.models import Tag
from workspaces.tags.serializers import TagSerializer

logger = logging.getLogger(__name__)

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    ordering = 'created_at'
