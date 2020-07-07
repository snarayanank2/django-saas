import logging
import jwt
import pytest
from tests.utils import assert_success, assert_error, assert_claim

logger = logging.getLogger(__name__)

def test_signin(db, client):
    res = client.post('/auth/basic/signin/', data={
	    'email': 'u1@gmail.com',
	    'password': 'password123'
    })
    assert_success(response=res, status_code=200)
    data = res.json()
    access_token = data['access_token']
    refresh_token = data['refresh_token']
    assert_claim(token=refresh_token, workspace_id=None, user_id=1)
    assert_claim(token=access_token, workspace_id=None, user_id=1)

def test_signin_fail(db, client):
    res = client.post('/auth/basic/signin/', data={
	    'email': 'u1@gmail.com',
	    'password': 'password124'
    })
    assert_error(response=res, status_code=401, detail='Unauthorized')

def test_signup(db, client):
    res = client.post('/auth/basic/signup/', data={
	    'email': 'u100@gmail.com',
	    'password': 'password124',
        'first_name': 'User100',
        'last_name': 'Earth'
    })
    assert_success(response=res, status_code=200)
    data = res.json()
    assert 'access_token' in data and 'refresh_token' in data

def test_signup_fail_user_exists(db, client):
    res = client.post('/auth/basic/signup/', data={
	    'email': 'u1@gmail.com',
	    'password': 'password124',
        'first_name': 'User100',
        'last_name': 'Earth'
    })
    assert_error(response=res, status_code=401, detail='Unauthorized')
