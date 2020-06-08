import logging

from rest_framework import serializers

from django_q.models import Schedule, Task

logger = logging.getLogger(__name__)

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['id', 'name', 'func', 'args', 'kwargs', 'schedule_type', 'repeats', 'next_run']
