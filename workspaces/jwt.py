from django.conf import settings
import logging
import jwt
from .models import Principal, Account
from .serializers import UserSerializer, AccountSerializer, WorkspaceSerializer, PrincipalSerializer
import datetime
from django.core import serializers
import threading
from jwt.exceptions import ExpiredSignatureError

logger = logging.getLogger(__name__)

class JWTUtils:
    secret_key = settings.SECRET_KEY
    refresh_token_exp = 60*60*24*30
    access_token_exp = 60*60
    _storage = threading.local()

    @classmethod
    def get_refresh_token(cls, principal_id):
        exp_seconds = cls.refresh_token_exp
        payload = {
            'principal_id': principal_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=exp_seconds)
        }
        return jwt.encode(payload, cls.secret_key, algorithm='HS256')

    @classmethod
    def get_access_token(cls, principal_id):
        exp_seconds = cls.access_token_exp
        principal = Principal.objects.get(id=principal_id)
        principal_data = PrincipalSerializer(instance=principal).data
        payload = {
            'principal': principal_data,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=exp_seconds)
        }
        encoded = jwt.encode(payload, cls.secret_key, algorithm='HS256')
        return encoded

    @classmethod
    def get_principal_from_refresh_token(cls, refresh_token):
        decoded = None
        try:
            decoded = jwt.decode(refresh_token, cls.secret_key, algorithms='HS256')
            principal_id = decoded['principal_id']
            principal = Principal.objects.get(id=principal_id)
            return principal
        except ExpiredSignatureError as e:
            logger.error('expired token')
            return None

    @classmethod
    def get_principal_from_access_token(cls, access_token):
        decoded = None
        try:
            decoded = jwt.decode(access_token, cls.secret_key, algorithms='HS256')
            principal = decoded['principal']
            return principal
        except ExpiredSignatureError as e:
            logger.error('expired token')
            return None

