from django_filters import rest_framework as filters
from saas_framework.comments.models import Comment

class ClosedSetFilter(filters.FilterSet):
    pass
    tag_name = filters.CharFilter(field_name='tags__name', lookup_expr='contains')
    message = filters.CharFilter(field_name='message', lookup_expr='contains')

    class Meta:
        model = Comment
        fields = ['tag_name', 'message']

