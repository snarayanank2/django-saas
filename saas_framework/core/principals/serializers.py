import logging

from rest_framework import serializers
from saas_framework.core.accounts.serializers import AccountSerializer
from saas_framework.core.tpas.serializers import ThirdPartyAppSerializer
from saas_framework.core.principals.models import Principal

logger = logging.getLogger(__name__)

class PrincipalSerializer(serializers.ModelSerializer):
    account = AccountSerializer()
    tpa = ThirdPartyAppSerializer()

    class Meta:
        model = Principal
        fields = ['id', 'account', 'tpa', 'roles']
