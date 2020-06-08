from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
import logging

logger = logging.getLogger(__name__)

def post_save_callback(sender, instance, created, **kwargs):
    logger.info('sender %s instance %s created %s kwargs %s', sender, instance, created, kwargs)
