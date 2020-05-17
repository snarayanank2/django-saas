from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Workspace, WorkspaceUser, Principal
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def user_save(sender, instance, created, **kwargs):
    if created:
        w = Workspace(name='Default', owner=instance)
        w.save()
        wu = WorkspaceUser(workspace=w, user=instance)
        wu.save()
