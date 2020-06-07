import logging

from django.db import models
from django_q.models import Schedule, Task
from workspaces.workspaces.models import Workspace, BaseModel

logger = logging.getLogger(__name__)

class WorkspaceSchedule(BaseModel):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='+')
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='+')

    class Meta:
        ordering = ['workspace']

    # TODO - fix this
    def create_schedule(self, *args, **kwargs):
        pass
        # workspace = self
        # kwargs_copy = kwargs.copy()
        # if 'repeats' not in kwargs_copy:
        #     kwargs_copy['repeats'] = 1
        # schedule = Schedule.objects.create(*args, **kwargs_copy)
        # WorkspaceSchedule.objects.create(workspace=workspace, schedule=schedule)

    @property
    def tasks(self):
        return Task.objects.filter(group=self.schedule.id)
