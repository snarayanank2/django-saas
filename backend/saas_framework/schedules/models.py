import logging

from django.db import models
from django_q.models import Schedule

logger = logging.getLogger(__name__)

# No code here - everything comes from django_q

def dummy_func(workspace_id):
    print(f'i am also printing this as dummy of workspace_id {workspace_id}')
    logger.info('hello - i am dummy task of workspace_id %s', workspace_id)