from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
import logging
from itertools import chain
from saas_framework.core.auth_utils import AuthUtils
import threading
from django.db.models.signals import post_save, post_delete
from saas_framework.tags.models import Tag

logger = logging.getLogger(__name__)


class ChangeHandler:
    track_models = []
    _storage = threading.local()

    @staticmethod
    def __to_dict(instance):
        opts = instance._meta
        data = {}
        for f in chain(opts.concrete_fields, opts.private_fields):
            data[f.name] = f.value_from_object(instance)
        for f in opts.many_to_many:
            data[f.name] = [i.id for i in f.value_from_object(instance)]
        return data

    @classmethod
    def register(cls):
        cls.track_models = [Tag]
        post_save.connect(cls.post_save_callback)
        post_delete.connect(cls.post_delete_callback)

    @classmethod
    def post_save_callback(cls, sender, instance, created, **kwargs):
        if sender in cls.track_models:
            logger.info('subject %s saved model %s instance %s created %s kwargs %s', 
            AuthUtils.get_current_principal_id(), sender, ChangeHandler.__to_dict(instance), created, kwargs)

    @classmethod
    def post_delete_callback(cls, sender, instance, **kwargs):
        if sender in cls.track_models:
            logger.info('subject %s deleted model %s instance %s kwargs %s', 
            AuthUtils.get_current_principal_id(), sender, ChangeHandler.__to_dict(instance), kwargs)
