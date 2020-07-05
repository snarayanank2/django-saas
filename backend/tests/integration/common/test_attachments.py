import logging
from tests.utils import assert_error, assert_success
import pytest

logger = logging.getLogger(__name__)

def test_list1(db, u1client):
    res = u1client.get('/common/attachments/')
    assert_success(response=res, status_code=200)
    data = res.json()
    assert data['count'] == 0

def test_upload_download_delete(db, u1client):
    filename = '/tmp/test.txt'
    with open(filename, 'w') as f:
        f.write('hello')

    with open(filename, 'r') as f:
        res = u1client.post('/common/attachments/', data={
            'file': f,
            'content_type': 'text/plain',
            'filename': 'test.txt'
        })
    assert_success(response=res, status_code=201)
    data = res.json()
    id = data['id']
    res = u1client.get(f'/common/attachments/{id}/download/')
    assert res.get('Content-Disposition') == 'attachment; filename="test.txt"'
    content = str(res.content, 'utf-8')
    assert content == 'hello'

    res = u1client.delete(f'/common/attachments/{id}/')
    assert res.status_code == 204

    res = u1client.get('/common/attachments/')
    assert_success(response=res, status_code=200)
    data = res.json()
    assert data['count'] == 0

def test_delete_fail(db, u1client):
    res = u1client.delete(f'/common/attachments/2323/')
    assert_error(response=res, status_code=404, detail='Not found')