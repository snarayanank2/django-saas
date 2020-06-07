from django.conf import settings
import logging
import jwt
import datetime
import threading
from jwt.exceptions import ExpiredSignatureError
from workspaces.principals.models import Principal

logger = logging.getLogger(__name__)

class JWTUtils:
    secret_key = settings.SECRET_KEY
    refresh_token_exp = 60*60*24*30
    access_token_exp = 60*60

    @classmethod
    def get_refresh_token(cls, principal_id):
        exp_seconds = cls.refresh_token_exp
        principal = Principal.objects.get(id=principal_id)
        claim = {
            'principal_id': principal.id
        }
        return cls.get_token_from_claim(claim=claim, exp_seconds=exp_seconds)

    @classmethod
    def get_access_token(cls, principal_id):
        exp_seconds = cls.access_token_exp
        principal = Principal.objects.get(id=principal_id)
        claim = {
            'principal_id': principal.id,
            'account_id': principal.account.id,
            'workspace_id': principal.account.workspace.id,
            'user_id': principal.account.user.id,
            'client_application_id': principal.client_application.id,
            'roles': principal.roles
        }
        return cls.get_token_from_claim(claim=claim, exp_seconds=exp_seconds)

    @classmethod
    def get_token_from_claim(cls, claim, exp_seconds):
        payload = {
            'claim' : claim,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=exp_seconds)
        }
        encoded = jwt.encode(payload, cls.secret_key, algorithm='HS256')
        return encoded

    @classmethod
    def get_claim_from_token(cls, token):
        decoded = None
        try:
            decoded = jwt.decode(token, cls.secret_key, algorithms='HS256')
            claim = decoded['claim']
            return claim
        except Exception as e:
            logger.error('unable to extract claim')
            return None


