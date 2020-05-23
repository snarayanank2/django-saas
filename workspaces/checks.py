from django.core.checks import Error, register
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

@register
def workspaces_checks(app_configs, **kwargs):
    errors = []
    missing_apps = list(set(['rest_framework', 'django_filters', 'django_q']) - set(settings.INSTALLED_APPS))
    if len(missing_apps) > 0:
        errors.append(
            Error(
                f'missing entries in INSTALLED_APPS {missing_apps}',
                obj=settings
            )
        )
    logger.info('Installed apps: %s', settings.INSTALLED_APPS)
    return errors