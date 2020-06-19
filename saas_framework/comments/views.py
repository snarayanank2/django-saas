import logging

from rest_framework import filters
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import viewsets
from saas_framework.comments.filters import CommentFilter
from saas_framework.comments.models import Comment
from saas_framework.comments.serializers import CommentSerializer
from saas_framework.closed_sets.mixins import ClosedSetMembershipModelViewSetMixin

logger = logging.getLogger(__name__)

class CommentViewSet(ClosedSetMembershipModelViewSetMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CommentFilter
    search_fields = ['message']
    ordering_fields = ['created_at']
    ordering = 'created_at'
