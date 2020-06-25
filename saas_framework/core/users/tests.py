import logging

import pytest
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

def test_count(db):
    num_users = User.objects.all().count()
    assert num_users == 10

def test_users(aclient):
    res = aclient.get('/admin/users/').json()
    logger.info('res = %s', res)

