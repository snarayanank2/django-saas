import logging
from tests.utils import assert_error, assert_success, assert_claim
import pytest

logger = logging.getLogger(__name__)

def test_list1(db, u1client):
    res = u1client.get('/auth/workspaces/')
    assert_success(response=res, status_code=200)
    data = res.json()
    assert data['count'] == 2

def test_list2(db, u2client):
    res = u2client.get('/auth/workspaces/')
    assert_success(response=res, status_code=200)
    data = res.json()
    assert data['count'] == 1

def test_create(db, u3client):
    res = u3client.post('/auth/workspaces/', data={
	    "name": "workspace3"
    })
    assert_success(response=res, status_code=201)
    data = res.json()
    assert data['name'] == 'workspace3'

def test_switch(db, u1client):
    res = u1client.post(f'/auth/workspaces/2/switch/')
    assert_success(response=res, status_code=200)
    data = res.json()
    assert 'access_token' in data and 'refresh_token' in data
    access_token = data['access_token']
    refresh_token = data['refresh_token']
    assert_claim(token=access_token, workspace_id=2)

def test_switch_fail(db, u1client):
    res = u1client.post(f'/auth/workspaces/12121/switch/')
    assert_error(response=res, status_code=401, detail='Unauthorized')
