import logging
import jwt
import pytest
from tests.utils import assert_claim

logger = logging.getLogger(__name__)

def test_signin(db, client):
    res = client.post('/auth/basic/signin/', data={
	    'email': 'u1@gmail.com',
	    'password': 'password123'
    })
    assert res.status_code == 200
    data = res.json()
    access_token = data['access_token']
    refresh_token = data['refresh_token']
    assert_claim(token=refresh_token, workspace_id=1, user_id=1)
    assert_claim(token=access_token, workspace_id=1, user_id=1)

def test_signin_fail(db, client):
    res = client.post('/auth/basic/signin/', data={
	    'email': 'u1@gmail.com',
	    'password': 'password124'
    })
    assert res.status_code == 401
    data = res.json()
    assert 'Unauthorized' in data['detail']
