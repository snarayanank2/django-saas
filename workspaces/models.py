import logging

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django_q.models import Task
from .auth import AuthUtils

logger = logging.getLogger(__name__)

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Workspace(BaseModel):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')

class WorkspaceTask(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    class Meta:
        ordering = ['workspace']

class WorkspaceUser(BaseModel):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=200)

    class Meta:
        ordering = ['workspace']

class Principal(BaseModel):
    workspace_user = models.ForeignKey(WorkspaceUser, on_delete=models.CASCADE)

    class Meta:
        ordering = ['workspace_user']

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
