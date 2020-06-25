import logging

import pytest
from saas_framework.core.workspaces.models import Workspace

logger = logging.getLogger(__name__)

def test_count(db):
    num = Workspace.objects.all().count()
    assert num == 10
