from django_filters import rest_framework as filters
from django.contrib.auth.models import User
from .models import WorkspaceUser, Comment

class WorkspaceUserFilter(filters.FilterSet):
    workspace_id = filters.NumberFilter(field_name='workspace_id')

    class Meta:
        model = WorkspaceUser
        fields = {
            'workspace_id': ['exact']
        }

class CommentFilter(filters.FilterSet):
    tag = filters.CharFilter(field_name='tags__name', lookup_expr='contains')
    message = filters.CharFilter(field_name='message', lookup_expr='contains')

    class Meta:
        model = Comment
        fields = ['tag', 'message']