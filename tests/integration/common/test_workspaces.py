import logging

import pytest

logger = logging.getLogger(__name__)

def test_list(db, u1client):
    res = u1client.get('/common/workspaces/')
    assert res.status_code == 200
    data = res.json()
    assert data['count'] == 1

