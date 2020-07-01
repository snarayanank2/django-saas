import logging
import jwt
import pytest
import re
from tests.utils import assert_claim, assert_response
from django.test import Client

logger = logging.getLogger(__name__)

def authorize(u1client):
    res = u1client.get('/auth/o/authorize/', data={'client_id': 2, 'response_type': 'code', 'state': 'yabba', 'redirect_uri': 'https://www.google.com/', 'scope': 'admin'})    
    assert res.status_code == 200
    data = res.json()
    assert 'redirect_uri' in data
    redirect_uri = data['redirect_uri']
    p = re.compile('.*code=(.*)&.*')
    m = p.match(redirect_uri)
    code = m.group(1)
    return code

def tokens(u1client, code):
    res = u1client.post('/auth/o/token/', data={'client_id': 2, 'client_secret': 'password123', 'code': code, 'state': 'yabba', 'grant_type': 'authorization_code'})
    assert res.status_code == 200
    data = res.json()
    assert 'access_token' in data
    assert 'refresh_token' in data
    return data['refresh_token'], data['access_token']

def test_authorize(u1client):
    code = authorize(u1client=u1client)
    assert code, 'code is null'
    assert_claim(token=code, tpa_id=2, user_id=1, workspace_id=1)

def test_authorize_fail_role(u3client):
    # u3 does not have admin role, therefore cannot authorize for scope admin
    res = u3client.get('/auth/o/authorize/', data={'client_id': 2, 'response_type': 'code', 'state': 'yabba', 'redirect_uri': 'https://www.google.com/', 'scope': 'admin'})
    assert_response(response=res, status_code=403, detail='You do not have')
 
def test_authorize_fail_response_type(u3client):
    res = u3client.get('/auth/o/authorize/', data={'client_id': 2, 'response_type': 'implicit', 'state': 'yabba', 'redirect_uri': 'https://www.google.com/', 'scope': 'admin'})    
    assert_response(response=res, status_code=400, detail='Invalid')

def test_refresh_token(u1client):
    code = authorize(u1client=u1client)
    refresh_token, access_token = tokens(u1client=u1client, code=code)
    assert_claim(token=refresh_token, tpa_id=2, user_id=1)
    assert_claim(token=access_token, tpa_id=2, user_id=1, roles='admin')

def test_refresh_token_fail_secret(u1client):
    code = authorize(u1client=u1client)
    res = u1client.post('/auth/o/token/', data={'client_id': 2, 'client_secret': 'blah', 'code': code, 'state': 'yabba', 'grant_type': 'authorization_code'})
    assert_response(response=res, status_code=401, detail='Unauthorized')

def test_access_token(u1client):
    code = authorize(u1client=u1client)
    refresh_token, access_token = tokens(u1client=u1client, code=code)
    res = u1client.post('/auth/o/token/', data={'client_id': 2, 'client_secret': 'password123', 'refresh_token': refresh_token, 'grant_type': 'refresh_token'})
    assert_response(response=res, status_code=200)
    data = res.json()
    assert 'refresh_token' in data
    assert 'access_token' in data
    assert_claim(token=access_token, tpa_id=2)

