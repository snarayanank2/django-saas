import logging

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http.response import HttpResponseForbidden
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from saas_framework.core.accounts.models import Account
from saas_framework.core.principals.models import Principal
from saas_framework.core.tpas.models import ThirdPartyApp
from saas_framework.core.tpas.views import OAuth2Authorize, OAuth2Token
from saas_framework.core.workspaces.models import Workspace
from saas_framework.core.auth.claim import Claim

logger = logging.getLogger(__name__)

class BasicAuthSigninView(APIView):
    def post(self, request):
        """
        Should return access_token, refresh_token
        """
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        user = authenticate(username=email, password=password)
        if user is None:
            raise AuthenticationFailed()
        app_name = request.data.get('app_name', 'webapp')
        tpa = ThirdPartyApp.objects.get(name=app_name)
        account = Account.objects.filter(user=user).order_by('-created_at').all()[0]
        # log into the oldest workspace by default
        (principal, created) = Principal.objects.get_or_create(account=account, tpa=tpa, roles=account.roles)
        claim = Claim(user_id=user.id, workspace_id=account.workspace.id, principal_id=principal.id, tpa_id=tpa.id, account_id=account.id, roles=account.roles)
        refresh_token = claim.to_token(exp_seconds=7*24*3600)
        access_token = claim.to_token(exp_seconds=600)
        return Response({ 'refresh_token': refresh_token, 'access_token': access_token })

class BasicAuthSignupView(APIView):
    def post(self, request):
        """
        Should return access_token, refresh_token
        """
        email = request.data.get('email', None)
        first_name = request.data.get('first_name', None)
        last_name = request.data.get('last_name', None)
        password = request.data.get('password', None) # should confirm password come here?
        if User.objects.filter(username=email).exists():
            raise PermissionDenied()
        user = User.objects.create(first_name=first_name, last_name=last_name, email=email, username=email, password=make_password(password))
        app_name = request.data.get('app_name', 'webapp')
        tpa = ThirdPartyApp.objects.get(name=app_name)
        workspace = Workspace.objects.create(name='Default')
        account = Account.objects.create(user=user, workspace=workspace, roles='admin')
        (principal, created) = Principal.objects.get_or_create(workspace=account.workspace, user=account.user, tpa=tpa)
        claim = Claim(user_id=user.id, workspace_id=workspace.id, principal_id=principal.id, tpa_id=tpa.id, account_id=account.id, roles=account.roles)
        refresh_token = claim.to_token(exp_seconds=7*24*3600)
        access_token = claim.to_token(exp_seconds=600)
        return Response({ 'refresh_token': refresh_token, 'access_token': access_token })

class RefreshTokenView(APIView):
    def post(self, request):
        """
        Should return access_token
        """
        claim = Claim.from_token(token=request.data.get('refresh_token', None))
        if not claim.user_id:
            raise PermissionDenied()

        # TODO: should check if account is disabled
        access_token = claim.to_token(exp_seconds=600)
        return Response({ 'access_token' : access_token })

class SwitchWorkspaceView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        workspace_id = request.data.get('workspace_id')
        claim = Claim.from_token(token=refresh_token)
        if not claim.user_id:
            raise PermissionDenied()
        principal = Principal.objects.get(id=claim.principal_id)
        workspace = Workspace.objects.get(id=workspace_id)
        account = Account.objects.get(workspace=workspace, user=principal.account.user)
        (principal, created) = Principal.objects.get_or_create(account=account, tpa=ThirdPartyApp.objects.get(id=claim.tpa_id), roles=account.roles)
        claim1 = Claim(principal_id=principal.id, user_id=principal.account.user.id, account_id=principal.account.id, workspace_id=principal.account.workspace.id, roles=principal.roles, tpa_id=principal.tpa.id)
        refresh_token = claim1.to_token(exp_seconds=7*24*3600)
        access_token = claim1.to_token(exp_seconds=600)
        return Response({ 'refresh_token': refresh_token, 'access_token': access_token })

class OAuth2Authorize(OAuth2Authorize):
    def get(self, request):
        logger.info('request_params %s', request.query_params)
        request.query_params._mutable = True
        request.query_params['workspace_id'] = request.claim.workspace_id
        request.query_params['account_id'] = request.claim.account_id
        request.query_params._mutable = False
        return super().get(request)

class OAuthToken(OAuth2Authorize):
    pass

class JwtDecode(APIView):
    def post(self, request):
        jwt = request.data['jwt']
        claim = Claim.from_token(token=jwt)
        return Response({ 'claim' : claim.__dict__ })
