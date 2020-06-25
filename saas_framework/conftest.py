import logging
import random

import pytest
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django_q.models import Schedule

from saas_framework.core.accounts.models import Account
from saas_framework.core.principals.models import Principal
from saas_framework.core.tpas.models import ThirdPartyApp
from saas_framework.core.workspace_membership.models import WorkspaceMembership
from saas_framework.core.workspaces.models import Workspace

logger = logging.getLogger(__name__)

def load():
    for i in range(0, 10):
        email = f'elonmusk{i}@yahoo.com'
        password='password123'
        u = User.objects.create(first_name='Elon', last_name='Musk', email=email, username=email, password=make_password(password))
        w = Workspace.objects.create(name='Default')
        schedule = Schedule.objects.create(name='dummy', func='saas_framework.tasks.workspace_summary', schedule_type=Schedule.ONCE, repeats=1)
        wm = WorkspaceMembership.objects.create(workspace=w, content_object=schedule)

    ThirdPartyApp.objects.create(user=User.objects.get(id=1), name='webapp', secret=make_password(password), 
                description='foo', enabled=True, redirect_uris='')

    for i in range(1, 100):
        uid = random.randint(1, 10)
        wid = random.randint(1, 10)
        u = User.objects.get(pk=uid)
        w = Workspace.objects.get(pk=wid)
        Account.objects.get_or_create(user=u, workspace=w, roles='admin,auditor,common')

@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    logger.info('setting up db')
    with django_db_blocker.unblock():
        load()
