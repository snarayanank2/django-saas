from django.apps import AppConfig
from django.db.models.signals import post_save

class WorkspacesConfig(AppConfig):
    name = 'workspaces'

    def ready(self):
        from .signals import user_save
        from django.contrib.auth.models import User
        post_save.connect(user_save, sender=User)