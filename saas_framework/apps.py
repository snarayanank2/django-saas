from django.apps import AppConfig
from django.db.models.signals import post_save

class SaaSConfig(AppConfig):
    name = 'saas_framework'

    def ready(self):
        from saas_framework.signals import post_save_callback
        from saas_framework.checks import workspaces_checks
        post_save.connect(post_save_callback)