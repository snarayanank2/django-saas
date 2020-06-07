import logging

from rest_framework import filters
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import viewsets
from workspaces.comments.filters import CommentFilter
from workspaces.comments.models import Comment
from workspaces.comments.serializers import CommentSerializer

logger = logging.getLogger(__name__)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CommentFilter
    search_fields = ['message']
    ordering_fields = ['created_at']
    ordering = 'created_at'
