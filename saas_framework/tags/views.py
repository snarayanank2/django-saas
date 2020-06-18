import logging


from rest_framework import viewsets
from saas_framework.tags.models import Tag
from saas_framework.tags.serializers import TagSerializer
from saas_framework.closed_sets.views import ClosedSetMembershipModelViewSetMixin

logger = logging.getLogger(__name__)

class TagViewSet(ClosedSetMembershipModelViewSetMixin, viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    ordering = 'created_at'
