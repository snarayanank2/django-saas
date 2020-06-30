import logging
import jwt
import pytest

logger = logging.getLogger(__name__)

def test_common_only(db, u3client):
    res = u3client.get('/admin/users/')
    assert res.status_code == 403
    data = res.json()
    assert 'Authentication credentials were not provided' in data['detail']
