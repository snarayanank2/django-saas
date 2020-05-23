import logging

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django_q.models import Schedule, Task
from .auth import AuthUtils

logger = logging.getLogger(__name__)

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class ClientApplication(BaseModel):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    class Meta:
        ordering = ['id']

def dummy_async_task():
    print('this is a dummy async task')

class Workspace(BaseModel):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')

    def create_schedule(self, *args, **kwargs):
        workspace = self
        kwargs_copy = kwargs.copy()
        if 'repeats' not in kwargs_copy:
            kwargs_copy['repeats'] = 1
        schedule = Schedule.objects.create(*args, **kwargs_copy)
#        logger.info('schedule = %s', schedule)
        WorkspaceSchedule.objects.create(workspace=workspace, schedule=schedule)


class WorkspaceSchedule(BaseModel):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)

    class Meta:
        ordering = ['workspace']

    @property
    def tasks(self):
        return Task.objects.filter(group=self.schedule.id)


class WorkspaceUser(BaseModel):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=200)

    class Meta:
        ordering = ['workspace']

class Principal(BaseModel):
    workspace_user = models.ForeignKey(WorkspaceUser, on_delete=models.CASCADE)
    client_application = models.ForeignKey(ClientApplication, on_delete=models.CASCADE)

    class Meta:
        ordering = ['workspace_user']

# This is the important class that others should inherit from

class WorkspaceBaseModel(BaseModel):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    created_by = models.ForeignKey(Principal, on_delete=models.CASCADE, related_name='+')
    updated_by = models.ForeignKey(Principal, on_delete=models.CASCADE, related_name='+')

    class Meta:
        abstract = True

class Tag(WorkspaceBaseModel):
    name = models.CharField(max_length=200)

class Attachment(WorkspaceBaseModel):
    file = models.FileField(blank=False, null=False)
    content_type = models.CharField(max_length=100)
    filename = models.CharField(max_length=200)

    def __str__(self):
        return self.file.name


class Comment(WorkspaceBaseModel):
    message = models.CharField(max_length=1024)
    tags = models.ManyToManyField(Tag)
    attachments = models.ManyToManyField(Attachment)
