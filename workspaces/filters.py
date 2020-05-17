from django_filters import rest_framework as filters
from django.contrib.auth.models import User
from .models import WorkspaceUser

class WorkspaceUserFilter(filters.FilterSet):
    workspace_id = filters.NumberFilter(field_name='workspace_id')

    class Meta:
        model = WorkspaceUser
        fields = {
            'workspace_id': ['exact']
        }
