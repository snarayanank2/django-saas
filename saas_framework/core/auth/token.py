import logging
from typing import Tuple

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated, ParseError, PermissionDenied

from saas_framework.core.accounts.models import Account
from saas_framework.core.auth.claim import Claim
from saas_framework.core.principals.models import Principal
from saas_framework.core.tpas.models import AccountThirdPartyApp, ThirdPartyApp
from saas_framework.core.workspaces.models import Workspace
from rest_framework.exceptions import APIException, NotFound

logger = logging.getLogger(__name__)

class UnAuthorizedException(APIException):
    status_code = 401
    default_detail = 'Unauthorized'
    default_code = 'unauthorized'

class TokenUtils:
    REFRESH_TOKEN_EXPIRY_SEC = 30*24*3600
    ACCESS_TOKEN_EXPIRY_SEC = 600

    @staticmethod
    def signin(email, password, app_name) -> Tuple[str, str]:
        user = None
        user = authenticate(username=email, password=password)
        if user is None:
            raise UnAuthorizedException()
        tpa = ThirdPartyApp.objects.get(name=app_name)
        account = Account.objects.filter(user=user).order_by('id').all()[0]
        # log into the oldest workspace by default
        (principal, created) = Principal.objects.get_or_create(account=account, tpa=tpa, roles=account.roles)
        claim = Claim(user_id=user.id, workspace_id=account.workspace.id, principal_id=principal.id, tpa_id=tpa.id, account_id=account.id, roles=account.roles)
        refresh_token = claim.to_token(exp_seconds=TokenUtils.REFRESH_TOKEN_EXPIRY_SEC)
        access_token = claim.to_token(exp_seconds=TokenUtils.ACCESS_TOKEN_EXPIRY_SEC)
        return (refresh_token, access_token)

    @staticmethod
    def signup(email, first_name, last_name, password, app_name) -> Tuple[str, str]:
        if User.objects.filter(username=email).exists():
            raise UnAuthorizedException()
        user = User.objects.create(first_name=first_name, last_name=last_name, email=email, username=email, password=make_password(password))
        tpa = ThirdPartyApp.objects.get(name=app_name)
        workspace = Workspace.objects.create(name='Default')
        account = Account.objects.create(user=user, workspace=workspace, roles='common,admin')
        (principal, created) = Principal.objects.get_or_create(workspace=account.workspace, user=account.user, tpa=tpa)
        claim = Claim(user_id=user.id, workspace_id=workspace.id, principal_id=principal.id, tpa_id=tpa.id, account_id=account.id, roles=account.roles)
        refresh_token = claim.to_token(exp_seconds=TokenUtils.REFRESH_TOKEN_EXPIRY_SEC)
        access_token = claim.to_token(exp_seconds=TokenUtils.ACCESS_TOKEN_EXPIRY_SEC)
        return (refresh_token, access_token)

    @staticmethod
    def access_token(refresh_token) -> str:
        claim = Claim.from_token(token=refresh_token)
        if not claim.user_id:
            raise UnAuthorizedException()

        # TODO: should check if account is disabled
        access_token = claim.to_token(exp_seconds=TokenUtils.ACCESS_TOKEN_EXPIRY_SEC)
        return access_token

    @staticmethod
    def switch_workspace(refresh_token, workspace_id) -> Tuple[str, str]:
        claim = Claim.from_token(token=refresh_token)
        if not claim.user_id:
            raise UnAuthorizedException()
        principal = Principal.objects.get(id=claim.principal_id)
        try:
            workspace = Workspace.objects.get(id=workspace_id)
        except ObjectDoesNotExist:
            raise NotFound()

        account = Account.objects.get(workspace=workspace, user=principal.account.user)
        (principal, created) = Principal.objects.get_or_create(account=account, tpa=ThirdPartyApp.objects.get(id=claim.tpa_id), roles=account.roles)
        claim1 = Claim(principal_id=principal.id, user_id=principal.account.user.id, account_id=principal.account.id, workspace_id=principal.account.workspace.id, roles=principal.roles, tpa_id=principal.tpa.id)
        refresh_token = claim1.to_token(exp_seconds=TokenUtils.REFRESH_TOKEN_EXPIRY_SEC)
        access_token = claim1.to_token(exp_seconds=TokenUtils.ACCESS_TOKEN_EXPIRY_SEC)
        return (refresh_token, access_token)

    @staticmethod
    def oauth2_code(claim, client_id, scope) -> str:
        if not claim.user_id:
            raise UnAuthorizedException()
        workspace = Workspace.objects.get(id=claim.workspace_id)
        account = Account.objects.get(id=claim.account_id)
        tpa = ThirdPartyApp.objects.get(id=client_id)
        extra_roles = set(scope.split(',')) - set(account.roles.split(','))
        if len(extra_roles) > 0:
            raise PermissionDenied()
        roles = scope
        atpa = AccountThirdPartyApp.objects.create(workspace=workspace, tpa=tpa, account=account, roles=roles)
        claim1 = Claim(atpa_id=atpa.id, tpa_id=tpa.id, workspace_id=workspace.id, account_id=account.id, user_id=account.user.id)
        code = claim1.to_token(exp_seconds=300)
        return code

    @staticmethod
    def oauth2_refresh_token(client_id, client_secret, code) -> Tuple[str, str]:
        tpa = ThirdPartyApp.objects.get(id=client_id)
        if not check_password(client_secret, tpa.secret):
            raise UnAuthorizedException()
        claim = Claim.from_token(token=code)
        atpa_id = claim.atpa_id
        atpa = AccountThirdPartyApp.objects.get(id=atpa_id)
        assert tpa == atpa.tpa
        (principal, created) = Principal.objects.get_or_create(account=atpa.account, tpa=atpa.tpa, roles=atpa.roles)
        claim1 = Claim(user_id=atpa.account.user.id, workspace_id=atpa.account.workspace.id, tpa_id=atpa.tpa.id, account_id=atpa.account.id, principal_id=principal.id, roles=atpa.roles)
        refresh_token = claim1.to_token(exp_seconds=TokenUtils.REFRESH_TOKEN_EXPIRY_SEC) # consider 10 years
        access_token = claim1.to_token(exp_seconds=TokenUtils.ACCESS_TOKEN_EXPIRY_SEC)
        return (refresh_token, access_token)

    @staticmethod
    def oauth2_access_token(client_id, client_secret, refresh_token) -> Tuple[str, str]:
        tpa = ThirdPartyApp.objects.get(id=client_id)
        if not check_password(client_secret, tpa.secret):
            raise UnAuthorizedException()
        claim = Claim.from_token(token=refresh_token)
        if not claim.user_id:
            raise UnAuthorizedException()
        principal_id = claim.principal_id
        principal = Principal.objects.get(id=principal_id)
        assert principal.tpa == tpa
        claim1 = Claim(principal_id=principal.id, user_id=principal.account.user.id, workspace_id=principal.account.workspace.id, account_id=principal.account.id, tpa_id=principal.tpa.id, roles=principal.roles)
        access_token = claim1.to_token(exp_seconds=TokenUtils.ACCESS_TOKEN_EXPIRY_SEC)
        return (refresh_token, access_token)
