import logging

from rest_framework import serializers
from saas_framework.tpas.models import ThirdPartyApp

logger = logging.getLogger(__name__)

class ThirdPartyAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThirdPartyApp
        fields = ['id', 'name']
