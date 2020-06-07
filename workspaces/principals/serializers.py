import logging

from rest_framework import serializers
from workspaces.accounts.serializers import AccountSerializer
from workspaces.tpas.serializers import ClientApplicationSerializer
from workspaces.principals.models import Principal

logger = logging.getLogger(__name__)

class PrincipalSerializer(serializers.ModelSerializer):
    account = AccountSerializer()
    client_application = ClientApplicationSerializer()

    class Meta:
        model = Principal
        fields = ['id', 'account', 'client_application', 'roles']
