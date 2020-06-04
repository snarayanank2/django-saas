import logging

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django_q.models import Schedule, Task
from workspaces.auth_utils import AuthUtils

logger = logging.getLogger(__name__)

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class ClientApplication(BaseModel):
    name = models.CharField(max_length=200)
    class Meta:
        ordering = ['id']

def dummy_async_task():
    print('this is a dummy async task')

class Workspace(BaseModel):
    name = models.CharField(max_length=200)

    def create_schedule(self, *args, **kwargs):
        workspace = self
        kwargs_copy = kwargs.copy()
        if 'repeats' not in kwargs_copy:
            kwargs_copy['repeats'] = 1
        schedule = Schedule.objects.create(*args, **kwargs_copy)
        WorkspaceSchedule.objects.create(workspace=workspace, schedule=schedule)

class WorkspaceSchedule(BaseModel):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='+')
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='+')

    class Meta:
        ordering = ['workspace']

    @property
    def tasks(self):
        return Task.objects.filter(group=self.schedule.id)

class Account(BaseModel):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='+')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    roles = models.CharField(max_length=200)

    class Meta:
        ordering = ['created_at']
        constraints = [
            models.UniqueConstraint(fields= ['workspace','user'], name='unique_account')
        ]

class Principal(BaseModel):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='+')
    client_application = models.ForeignKey(ClientApplication, on_delete=models.CASCADE, related_name='+')
    roles = models.CharField(max_length=200)
    class Meta:
        ordering = ['created_at']

# This is the important class that others should inherit from

class WorkspaceBaseModel(BaseModel):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='+')

    def save(self, *args, **kwargs):
        principal = Principal.objects.get(id=AuthUtils.get_current_principal_id())
        if not principal:
            logger.warning('unknown principal making changes')
        if principal and self._state.adding:
            self.workspace = principal.account.workspace
        super().save(*args, **kwargs)

    class Meta:
        abstract = True

class Tag(WorkspaceBaseModel):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

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

    def __str__(self):
        return self.id
