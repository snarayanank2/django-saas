from django.apps import AppConfig
from django.db.models.signals import post_save

class WorkspacesConfig(AppConfig):
    name = 'workspaces'

    def ready(self):
        from workspaces.crud.signals import post_save_callback

        from django.contrib.auth.models import User
        from .checks import workspaces_checks
        post_save.connect(post_save_callback)