import logging

import pytest

logger = logging.getLogger(__name__)

def test_list(db, aclient):
    res = aclient.get('/common/workspaces/')
    assert res.status_code == 200
    data = res.json()
    assert data['count'] > 3

