import datetime
import json
import logging
import threading
from itertools import chain

from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from saas_framework.attachments.models import Attachment
from saas_framework.comments.models import Comment
from saas_framework.core.auth_utils import AuthUtils
from saas_framework.core.workspace_membership.models import WorkspaceMembership
from saas_framework.tags.models import Tag
from django.contrib.contenttypes.fields import GenericForeignKey

logger = logging.getLogger(__name__)


class ChangeHandler:
    track_models = []
    _storage = threading.local()

    @staticmethod
    def __instance_to_dict(instance):
        opts = instance._meta
        data = {}
        for f in chain(opts.concrete_fields, opts.private_fields):
            if not isinstance(f, GenericForeignKey):
                data[f.name] = f.value_from_object(instance)
        for f in opts.many_to_many:
            if not isinstance(f, GenericForeignKey):
                data[f.name] = [i.id for i in f.value_from_object(instance)]
        return data

    @staticmethod
    def __json_encoder(o):
        if isinstance(o, (datetime.date, datetime.datetime)):
            return o.isoformat()

    @staticmethod
    def __instance_to_json(instance):
        d = ChangeHandler.__instance_to_dict(instance)
        s = json.dumps(d, default=ChangeHandler.__json_encoder)
        return s

    @classmethod
    def register(cls):
        cls.track_models = [Tag, Attachment, Comment, WorkspaceMembership]
        post_save.connect(cls.post_save_callback)
        post_delete.connect(cls.post_delete_callback)

    @classmethod
    def post_save_callback(cls, sender, instance, created, **kwargs):
        if sender in cls.track_models:
            j = ChangeHandler.__instance_to_json(instance)
            logger.info('subject %s saved model %s instance %s created %s kwargs %s', 
            AuthUtils.get_current_principal_id(), sender, j, created, kwargs)

    @classmethod
    def post_delete_callback(cls, sender, instance, **kwargs):
        if sender in cls.track_models:
            j = ChangeHandler.__instance_to_json(instance)
            logger.info('subject %s deleted model %s instance %s kwargs %s', 
            AuthUtils.get_current_principal_id(), sender, j, kwargs)
