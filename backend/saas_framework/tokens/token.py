import logging
from typing import Tuple

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated, ParseError, PermissionDenied

from saas_framework.roles.models import Role
from saas_framework.tokens.claim import Claim
from saas_framework.tpas.models import ThirdPartyAppInstall, ThirdPartyApp
from saas_framework.workspaces.models import Workspace
from rest_framework.exceptions import APIException, NotFound
import hashlib
import base64

logger = logging.getLogger(__name__)

class UnAuthorizedException(APIException):
    status_code = 401
    default_detail = 'Unauthorized'
    default_code = 'unauthorized'

class TokenUtils:
    REFRESH_TOKEN_EXPIRY_SEC = 30*24*3600
    ACCESS_TOKEN_EXPIRY_SEC = 600

    @staticmethod
    def signin(email, password) -> Tuple[str, str]:
        user = None
        user = authenticate(username=email, password=password)
        if user is None:
            raise UnAuthorizedException()
        claim = Claim(user_id=user.id)
        refresh_token = claim.to_token(exp_seconds=TokenUtils.REFRESH_TOKEN_EXPIRY_SEC)
        access_token = claim.to_token(exp_seconds=TokenUtils.ACCESS_TOKEN_EXPIRY_SEC)
        return (refresh_token, access_token)

    @staticmethod
    def signup(email, first_name, last_name, password) -> Tuple[str, str]:
        if User.objects.filter(username=email).exists():
            raise UnAuthorizedException()
        user = User.objects.create(first_name=first_name, last_name=last_name, email=email, username=email, password=make_password(password))
        claim = Claim(user_id=user.id)
        refresh_token = claim.to_token(exp_seconds=TokenUtils.REFRESH_TOKEN_EXPIRY_SEC)
        access_token = claim.to_token(exp_seconds=TokenUtils.ACCESS_TOKEN_EXPIRY_SEC)
        return (refresh_token, access_token)

    @staticmethod
    def access_token(refresh_token) -> str:
        claim = Claim.from_token(token=refresh_token)
        if not claim.user_id:
            raise UnAuthorizedException()

        # TODO: should check if role is disabled
        access_token = claim.to_token(exp_seconds=TokenUtils.ACCESS_TOKEN_EXPIRY_SEC)
        return access_token

    @staticmethod
    def switch_workspace(user_id, workspace_id) -> Tuple[str, str]:
        if not user_id or not workspace_id:
            raise UnAuthorizedException()
        user = None
        workspace = None
        role = None
        try:
            user = User.objects.get(id=user_id)
            workspace = Workspace.objects.get(id=workspace_id)
            role = Role.objects.get(workspace=workspace, user=user)
        except ObjectDoesNotExist:
            raise UnAuthorizedException()

        claim = Claim(user_id=user.id, workspace_id=workspace.id, scope=role.scope)
        refresh_token = claim.to_token(exp_seconds=TokenUtils.REFRESH_TOKEN_EXPIRY_SEC)
        access_token = claim.to_token(exp_seconds=TokenUtils.ACCESS_TOKEN_EXPIRY_SEC)
        return (refresh_token, access_token)

    @staticmethod
    def oauth2_code(claim, client_id, scope, code_challenge) -> str:
        if not claim.user_id:
            raise UnAuthorizedException()
        if not claim.workspace_id:
            raise UnAuthorizedException('Workspace to link is not specified')
        workspace = Workspace.objects.get(id=claim.workspace_id)
        user = User.objects.get(id=claim.user_id)
        role = Role.objects.get(workspace=workspace, user=user)
        tpa = ThirdPartyApp.objects.get(id=client_id)
        extra_scope = set(scope.split(',')) - set(role.scope.split(','))
        if len(extra_scope) > 0:
            raise PermissionDenied(f'Requested scopes {extra_scope} cannot be granted by user')
        atpa = ThirdPartyAppInstall.objects.create(workspace=workspace, user=user, tpa=tpa)
        claim1 = Claim(user_id=user.id, tpa_id=tpa.id, workspace_id=workspace.id, scope=scope, code_challenge=code_challenge)
        code = claim1.to_token(exp_seconds=300)
        return code

    @staticmethod
    def generate_code_challenge(code_verifier):
        assert 43 <= len(code_verifier) <= 128, 'code_verifier string should be between 43 and 128 chars'
        hashed = hashlib.sha256(code_verifier.encode('ascii')).digest()
        encoded = base64.urlsafe_b64encode(hashed)
        code_challenge = encoded.decode('ascii')[:-1]
        return code_challenge

    @staticmethod
    def check_code_verifier(code_challenge, code_verifier):
        if not 43 <= len(code_verifier) <= 128:
            return False
        code_challenge1 = TokenUtils.generate_code_challenge(code_verifier=code_verifier)
        logger.info('code_challenge = %s, code_challenge1 = %s', code_challenge, code_challenge1)
        return code_challenge == code_challenge1

    @staticmethod
    def oauth2_refresh_token(client_id, code, client_secret, code_verifier) -> Tuple[str, str]:
        if not client_secret and not code_verifier:
            raise UnAuthorizedException("Must specify client_secret or code_verifier")
        if client_secret and code_verifier:
            raise ParseError('Cannot specify both client_secret and code_verifier')

        claim = Claim.from_token(token=code)
        tpa = ThirdPartyApp.objects.get(id=client_id)
        if client_secret:
            if not check_password(client_secret, tpa.secret):
                raise UnAuthorizedException()
        else:
            if not TokenUtils.check_code_verifier(code_challenge=claim.code_challenge, code_verifier=code_verifier):
                raise UnAuthorizedException("Invalid code_verifier")
        tpa = ThirdPartyApp.objects.get(id=claim.tpa_id)
        workspace = Workspace.objects.get(id=claim.workspace_id)
        user = User.objects.get(id=claim.user_id)
        try:
            atpa = ThirdPartyAppInstall.objects.get(workspace=workspace, user=user, tpa=tpa)
        except ObjectDoesNotExist:
            raise PermissionDenied()

        claim1 = Claim(user_id=user.id, workspace_id=workspace.id, tpa_id=tpa.id, scope=claim.scope, code_challenge=claim.code_challenge)
        refresh_token = claim1.to_token(exp_seconds=TokenUtils.REFRESH_TOKEN_EXPIRY_SEC) # consider 10 years
        access_token = claim1.to_token(exp_seconds=TokenUtils.ACCESS_TOKEN_EXPIRY_SEC)
        return (refresh_token, access_token)

    @staticmethod
    def oauth2_access_token(client_id, client_secret, refresh_token, code_verifier) -> Tuple[str, str]:
        if not client_secret and not code_verifier:
            raise UnAuthorizedException("Must specify client_secret or code_verifier")
        if client_secret and code_verifier:
            raise ParseError('Cannot specify both client_secret and code_verifier')

        tpa = ThirdPartyApp.objects.get(id=client_id)
        claim = Claim.from_token(token=refresh_token)
        if client_secret:
            if not check_password(client_secret, tpa.secret):
                raise UnAuthorizedException()
        else:
            if not TokenUtils.check_code_verifier(code_challenge=claim.code_challenge, code_verifier=code_verifier):
                raise UnAuthorizedException("Invalid code_verifier")
        access_token = claim.to_token(exp_seconds=TokenUtils.ACCESS_TOKEN_EXPIRY_SEC)
        return (refresh_token, access_token)
