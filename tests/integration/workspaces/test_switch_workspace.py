import logging
import jwt
import pytest
from tests.utils import assert_success, assert_error, assert_claim

logger = logging.getLogger(__name__)

def test_switch_workspace(db, u1client):
    res = u1client.post(f'/workspaces/2/switch/')
    assert_success(response=res, status_code=200)
    data = res.json()
    assert 'access_token' in data and 'refresh_token' in data
    access_token = data['access_token']
    refresh_token = data['refresh_token']
    assert_claim(token=access_token, workspace_id=2)

def test_switch_workspace_fail(db, u1client):
    res = u1client.post(f'/workspaces/12121/switch/')
    assert_error(response=res, status_code=401, detail='Unauthorized')
