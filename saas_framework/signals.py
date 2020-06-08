from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def post_save_callback(sender, instance, created, **kwargs):
    logger.info('sender %s instance %s created %s kwargs %s', sender, instance, created, kwargs)
    # if created:
    #     w = Workspace(name='Default', owner=instance)
    #     w.save()
    #     wu = Account(workspace=w, user=instance, role='admin')
    #     wu.save()
