import datetime
import logging

from django.conf import settings

import jwt
from jwt.exceptions import ExpiredSignatureError

logger = logging.getLogger(__name__)


class Claim:
    secret_key = settings.SECRET_KEY

    def __init__(self, user_id=None, workspace_id=None, tpa_id=None, scope=None, code_challenge=None):
        self.workspace_id = workspace_id
        self.user_id = user_id
        self.tpa_id = tpa_id
        self.scope = scope
        self.code_challenge = code_challenge

    @classmethod
    def from_token(cls, token):
        decoded = None
        try:
            decoded = jwt.decode(token, cls.secret_key, algorithms='HS256')
            claim = Claim(**(decoded['claim']))
            return claim
        except Exception as e:
#            logger.error('unable to extract claim')
            return Claim.empty()

    def to_token(self, exp_seconds):
        claim_d = {
            'workspace_id': self.workspace_id,
            'user_id': self.user_id,
            'tpa_id': self.tpa_id,
            'scope': self.scope,
            'code_challenge': self.code_challenge
        }
        payload = {
            'claim' : claim_d,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=exp_seconds)
        }
        encoded = jwt.encode(payload, Claim.secret_key, algorithm='HS256')
        return str(encoded, 'utf8')

    @staticmethod
    def empty():
        return Claim()
