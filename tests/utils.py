import jwt
import logging

logger = logging.getLogger(__name__)

def assert_claim(token, **kwargs):
    payload = jwt.decode(token, verify=False)
    claim = payload['claim']
    for k in kwargs:
        v = kwargs[k]
        assert claim[k] == v, f'expected claim[{k}] to have {v}, but it had {claim[k]}'

def assert_success(response, status_code=None):
    data = response.json()
    assert not status_code or response.status_code == status_code, f'expected status_code {status_code} but got {response.status_code} with detail {data}'

def assert_error(response, status_code=None, detail=None):
    assert not status_code or response.status_code == status_code, f'expected status_code {status_code} but got {response.status_code}'
    if detail:
        data = response.json()
        assert 'detail' in data
        assert detail in data['detail'], f'expected to see {detail}, but got {data["detail"]}'
