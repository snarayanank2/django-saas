import logging
import jwt
import pytest

logger = logging.getLogger(__name__)

def assert_access_token(access_token, workspace_id=None, user_id=None):
    payload = jwt.decode(access_token, verify=False)
    claim = payload['claim']
    if workspace_id is not None:
        assert claim['workspace_id'] == workspace_id
    if user_id is not None:
        assert claim['user_id'] == user_id


def test_signin(db, client):
    res = client.post('/auth/basic/signin/', data={
	    'email': 'u1@gmail.com',
	    'password': 'password123'
    })
    assert res.status_code == 200
    data = res.json()
    access_token = data['access_token']
    refresh_token = data['refresh_token']
    payload = jwt.decode(access_token, verify=False)
    claim = payload['claim']
    assert claim['workspace_id'] == 1

def test_signin_fail(db, client):
    res = client.post('/auth/basic/signin/', data={
	    'email': 'u1@gmail.com',
	    'password': 'password124'
    })
    assert res.status_code == 401
    data = res.json()
    assert 'Unauthorized' in data['detail']
