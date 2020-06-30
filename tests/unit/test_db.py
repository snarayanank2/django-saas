import logging

import pytest
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

def test_user_count(db):
    num_users = User.objects.all().count()
    assert num_users == 10


