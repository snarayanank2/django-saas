from django_filters import rest_framework as filters
from workspaces.comments.models import Comment

class CommentFilter(filters.FilterSet):
    tag_name = filters.CharFilter(field_name='tags__name', lookup_expr='contains')
    message = filters.CharFilter(field_name='message', lookup_expr='contains')

    class Meta:
        model = Comment
        fields = ['tag_name', 'message']

