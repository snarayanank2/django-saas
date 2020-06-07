import logging

from rest_framework import serializers
from workspaces.tpas.models import ClientApplication

logger = logging.getLogger(__name__)

class ClientApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientApplication
        fields = ['id', 'name']
