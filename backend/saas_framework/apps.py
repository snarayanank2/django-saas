from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete

class SaaSConfig(AppConfig):
    name = 'saas_framework'

    def ready(self):
        from saas_framework.signals import ChangeHandler
        from saas_framework.checks import workspaces_checks
        ChangeHandler.register()
