import logging

from django.db import models
from django_q.models import Schedule
from saas_framework.workspaces.models import Workspace, BaseModel

logger = logging.getLogger(__name__)

class WorkspaceSchedule(BaseModel):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='+')
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='+')

    class Meta:
        ordering = ['workspace']

    @classmethod
    def create_schedule(cls, workspace, *args, **kwargs):
        task_kwargs = kwargs.copy()
        schedule_keys = ['func', 'name', 'hook', 'schedule_type', 'minutes', 'repeats', 'next_run', 'q_options']
        schedule_kwargs = {}
        for k in schedule_keys:
            if k in task_kwargs:
                schedule_kwargs[k] = task_kwargs[k]
                del task_kwargs[k]
        if 'repeats' not in schedule_kwargs:
            schedule_kwargs['repeats'] = 1
        task_kwargs['workspace_id'] = workspace.id
        schedule = Schedule.objects.create(*args, **schedule_kwargs, kwargs=task_kwargs)
        return WorkspaceSchedule.objects.create(workspace=workspace, schedule=schedule)

    # @property
    # def tasks(self):
    #     return Task.objects.filter(group=self.schedule.id)
