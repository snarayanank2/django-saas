import logging
from tests.utils import assert_error, assert_success
import pytest

logger = logging.getLogger(__name__)

def test_list1(db, u1client):
    res = u1client.get('/tpas/')
    assert_success(response=res, status_code=200)
    data = res.json()
    assert data['count'] == 2

def test_list2(db, u2client):
    res = u2client.get('/tpas/')
    assert_success(response=res, status_code=200)
    data = res.json()
    assert data['count'] == 0

def test_create(db, u3client):
    res = u3client.post('/tpas/', data={
	    'name': 'supertpa',
        'description': 'most awesome tpa ever',
        'enabled': True,
        'redirect_uris': 'https://www.google.com/',
        'secret': 'supertpa'
    })
    assert_success(response=res, status_code=201)
    data = res.json()
