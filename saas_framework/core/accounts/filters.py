from django_filters import rest_framework as filters
from saas_framework.core.accounts.models import Account

class AccountFilter(filters.FilterSet):
    workspace_id = filters.NumberFilter(field_name='workspace_id')

    class Meta:
        model = Account
        fields = {
            'workspace_id': ['exact']
        }

