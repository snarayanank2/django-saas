import logging

from rest_framework import viewsets
from django_q.models import Schedule
from saas_framework.schedules.serializers import ScheduleSerializer

logger = logging.getLogger(__name__)

class ScheduleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    ordering = 'created_at'
