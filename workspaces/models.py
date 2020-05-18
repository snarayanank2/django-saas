from django.db import models
from .auth import AuthUtils

# Create your models here.

from django.contrib.auth.models import User
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Workspace(BaseModel):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')

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

class Comment(WorkspaceBaseModel):
    message = models.CharField(max_length=1024)
    tags = models.ManyToManyField(Tag, related_name="comments")
