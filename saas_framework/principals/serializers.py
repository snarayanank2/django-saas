import logging

from rest_framework import serializers
from saas_framework.accounts.serializers import AccountSerializer
from saas_framework.tpas.serializers import ThirdPartyAppSerializer
from saas_framework.principals.models import Principal

logger = logging.getLogger(__name__)

class PrincipalSerializer(serializers.ModelSerializer):
    account = AccountSerializer()
    tpa = ThirdPartyAppSerializer()

    class Meta:
        model = Principal
        fields = ['id', 'account', 'tpa', 'roles']
