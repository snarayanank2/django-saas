import logging

from rest_framework import viewsets
from saas_framework.teams.models import Team
from saas_framework.teams.serializers import TeamSerializer
from django.db.models.expressions import Exists, OuterRef
from saas_framework.principals.models import Principal
#from django.utils import timezone

logger = logging.getLogger(__name__)

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    ordering = 'created_at'

