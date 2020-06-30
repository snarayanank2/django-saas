import logging

import pytest

logger = logging.getLogger(__name__)

def test_signin(db, client):
    res = client.post('/auth/basic/signin/', data={
	    'email': 'u1@gmail.com',
	    'password': 'password123'
    })
    assert res.status_code == 200
    data = res.json()
    assert 'access_token' in data and 'refresh_token' in data

def test_signin_fail(db, client):
    res = client.post('/auth/basic/signin/', data={
	    'email': 'u1@gmail.com',
	    'password': 'password124'
    })
    assert res.status_code == 401
    data = res.json()
    assert 'Unauthorized' in data['detail']


def test_switch_workspace(db, client):
    res = client.post('/auth/basic/signin/', data={
	    'email': 'u1@gmail.com',
	    'password': 'password123'
    })
    data = res.json()
    refresh_token = data['refresh_token']
    res = client.post('/auth/switch_workspace/', data={ 'refresh_token': refresh_token, 'workspace_id': 2})
    assert res.status_code == 200
    data = res.json()
    assert 'access_token' in data and 'refresh_token' in data
    # TODO: check if new access token is for new workspace