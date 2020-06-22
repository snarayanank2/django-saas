import logging

from django.db import models
from django_q.models import Schedule
from saas_framework.core.workspaces.models import Workspace, BaseModel

logger = logging.getLogger(__name__)

# No code here - everything comes from django_q
