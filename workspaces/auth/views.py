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
from workspaces.auth_utils import AuthUtils
from workspaces.tpas.models import ClientApplication
from workspaces.accounts.models import Account
from workspaces.principals.models import Principal
from workspaces.jwt import JWTUtils
from workspaces.workspaces.models import Workspace

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
        client_application = ClientApplication.objects.get(name=app_name)
        account = Account.objects.filter(user=user).order_by('-created_at').all()[0]
        # log into the oldest workspace by default
        (principal, created) = Principal.objects.get_or_create(account=account, client_application=client_application, roles=account.roles)
        refresh_token = JWTUtils.get_refresh_token(principal_id=principal.id)
        access_token = JWTUtils.get_access_token(principal_id=principal.id)
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
        client_application = ClientApplication.objects.get(name=app_name)
        workspace = Workspace.objects.create(name='Default')
        account = Account.objects.create(user=user, workspace=workspace, roles='admin')
        (principal, created) = Principal.objects.get_or_create(workspace=account.workspace, user=account.user, client_application=client_application)
        refresh_token = JWTUtils.get_refresh_token(principal_id=AuthUtils.get_current_principal_id())
        access_token = JWTUtils.get_access_token(principal_id=AuthUtils.get_current_principal_id())
        return Response({ 'refresh_token': refresh_token, 'access_token': access_token })

class RefreshTokenView(APIView):
    def post(self, request):
        """
        Should return access_token
        """
        claim = JWTUtils.get_claim_from_token(token=request.data.get('refresh_token', None))
        if not claim:
            raise PermissionDenied()
        principal_id = claim['principal_id']
        access_token = JWTUtils.get_access_token(principal_id=principal_id)
        return Response({ 'access_token' : access_token })

class SwitchWorkspaceView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        workspace_id = request.data.get('workspace_id')
        claim = JWTUtils.get_claim_from_token(token=refresh_token)
        if not claim:
            raise PermissionDenied()
        principal = Principal.objects.get(id=claim['principal_id'])
        workspace = Workspace.objects.get(id=workspace_id)
        account = Account.objects.get(workspace=workspace, user=principal.account.user)
        (principal, created) = Principal.objects.get_or_create(account=account, client_application=ClientApplication.objects.get(id=AuthUtils.get_current_client_application_id()), roles=account.roles)
        refresh_token = JWTUtils.get_refresh_token(principal_id=principal.id)
        access_token = JWTUtils.get_access_token(principal_id=principal.id)
        return Response({ 'refresh_token': refresh_token, 'access_token': access_token })
