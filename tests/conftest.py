import logging
import os
import random
import re

import pytest
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.test import Client
from django_q.models import Schedule

from saas_framework.tpas.models import ThirdPartyApp
from saas_framework.sharing.models import Sharing
from saas_framework.workspaces.models import Workspace
from saas_framework.roles.models import Role

logger = logging.getLogger(__name__)

def load():
    password = make_password('password123')
    u1 = User.objects.create(first_name='User1', last_name='Earth', email='u1@gmail.com', username='u1@gmail.com', password=password)
    u2 = User.objects.create(first_name='User2', last_name='Earth', email='u2@gmail.com', username='u2@gmail.com', password=password)
    u3 = User.objects.create(first_name='User3', last_name='Earth', email='u3@gmail.com', username='u3@gmail.com', password=password)

    w1 = Workspace.objects.create(name='workspace1')
    w2 = Workspace.objects.create(name='workspace2')

    r1 = Role.objects.get_or_create(user=u1, workspace=w1, scope='admin,common')
    r2 = Role.objects.get_or_create(user=u1, workspace=w2, scope='admin,common')
    r3 = Role.objects.get_or_create(user=u2, workspace=w2, scope='admin,common')
    r4 = Role.objects.get_or_create(user=u3, workspace=w1, scope='common')

    tpa1 = ThirdPartyApp.objects.create(creator=User.objects.get(id=1), name='webapp', secret=password, 
                description='tpa1', enabled=True, redirect_uris='')

    tpa2 = ThirdPartyApp.objects.create(creator=User.objects.get(id=1), name='tpa2', secret=password, 
                description='tpa2', enabled=True, redirect_uris='')

@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker, django_db_modify_db_settings, django_db_keepdb):
    from django.conf import settings
    # logger.info('setting up db reuse = %s', django_db_keepdb)
    # settings.DATABASES = {
    #     'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': 'db_test1.sqlite3' }
    # }
    # logger.info("DATABASES = %s", settings.DATABASES)
    # logger.info("DEFAULT_FILE_STORAGE = %s", settings.DEFAULT_FILE_STORAGE)
    # if not django_db_keepdb:
    #     with django_db_blocker.unblock():
    #         load()
    with django_db_blocker.unblock():
        load()


def login(client, email, password, switch_workspace=True):
    res = client.post('/identity/basic/signin/', data={
	    "email": email,
	    "password": password
    }).json()
    access_token = res['access_token']
    refresh_token = res['refresh_token']
    authorization = f'Bearer {access_token}'
    s = Client(HTTP_AUTHORIZATION=authorization)

    if switch_workspace:
        # pick first workspace
        res = s.get('/workspaces/')
        data = res.json()
        logger.info('data = %s', data)
        workspace_id = data['results'][0]['id']
        res = s.post(f'/workspaces/{workspace_id}/switch/', data={ 'refresh_token': refresh_token, 'workspace_id': workspace_id})
        data = res.json()
        assert 'access_token' in data and 'refresh_token' in data
        access_token = data['access_token']
        refresh_token = data['refresh_token']
        authorization = f'Bearer {access_token}'
        s1 = Client(HTTP_AUTHORIZATION=authorization)
        return s1

    return s

@pytest.fixture
def u1client(db, client):
    return login(client=client, email='u1@gmail.com', password='password123')

@pytest.fixture
def u2client(db, client):
    return login(client=client, email='u2@gmail.com', password='password123')

@pytest.fixture
def u3client(db, client):
    return login(client=client, email='u3@gmail.com', password='password123')
