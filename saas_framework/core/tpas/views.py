import logging

from django.contrib.auth.hashers import make_password
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from saas_framework.core.accounts.models import Account
from saas_framework.core.claim import Claim
from saas_framework.core.principals.models import Principal
from saas_framework.core.tpas.models import AccountThirdPartyApp, ThirdPartyApp
from saas_framework.core.tpas.serializers import (
    AccountThirdPartyAppSerializer, ThirdPartyAppSerializer)
from saas_framework.core.workspaces.models import Workspace

logger = logging.getLogger(__name__)

class ThirdPartyAppViewSet(viewsets.ModelViewSet):
    queryset = ThirdPartyApp.objects.all()
    serializer_class = ThirdPartyAppSerializer
    ordering = 'created_at'

class AccountThirdPartyAppViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AccountThirdPartyApp.objects.all()
    serializer_class = AccountThirdPartyAppSerializer
    ordering = 'created_at'

class OAuth2Authorize(APIView):
    def create_code_redirect_uri(self, workspace_id, account_id, client_id, scope, redirect_uri, state):
        workspace = Workspace.objects.get(id=workspace_id)
        account = Account.objects.get(id=account_id)
        tpa = ThirdPartyApp.objects.get(id=client_id)
        extra_roles = set(scope.split(',')) - set(account.roles.split(','))
        if len(extra_roles) > 0:
            raise PermissionDenied()
        roles = scope
        atpa = AccountThirdPartyApp.objects.create(workspace=workspace, tpa=tpa, account=account, roles=roles)
        claim = Claim(atpa_id=atpa.id)
        code = claim.to_token(exp_seconds=300)
        return redirect_uri + f'?code={code}&state={state}'

    def get(self, request):
        workspace_id = request.query_params.get('workspace_id')
        account_id = request.query_params.get('account_id')
        client_id = request.query_params.get('client_id')
        response_type = request.query_params.get('response_type')
        assert response_type in ['code']
        state = request.query_params.get('state', '')
        redirect_uri = request.query_params.get('redirect_uri')
        scope = request.query_params.get('scope')
        redirect_uri = self.create_code_redirect_uri(workspace_id=workspace_id, account_id=account_id, client_id=client_id, scope=scope, state=state, redirect_uri=redirect_uri)
        return Response({ 'redirect_uri' : redirect_uri })

class OAuth2Token(APIView):
    def process_code(self, client_id, client_secret, code):
        tpa = ThirdPartyApp.objects.get(id=client_id)
        logger.info('tpa.secret = %s, client_secret = %s', tpa.secret, client_secret)
        if tpa.secret != client_secret:
            logger.info('secrets dont match')
            raise PermissionDenied()
        claim = Claim.from_token(token=code)
        logger.info('claim = %s', claim)
        atpa_id = claim.atpa_id
        atpa = AccountThirdPartyApp.objects.get(id=atpa_id)
        assert tpa == atpa.tpa
        (principal, created) = Principal.objects.get_or_create(account=atpa.account, tpa=atpa.tpa, roles=atpa.roles)
        claim = Claim(user_id=atpa.account.user.id, workspace_id=atpa.account.workspace.id, tpa_id=atpa.tpa.id, account_id=atpa.account.id, principal_id=principal.id, roles=atpa.roles)
        refresh_token = claim.to_token(exp_seconds=30*24*3600) # consider 10 years
        access_token = claim.to_token(exp_seconds=3600)
        return (refresh_token, access_token)

    def process_refresh_token(self, client_id, client_secret, refresh_token):
        tpa = ThirdPartyApp.objects.get(id=client_id)
        if tpa.secret != make_password(client_secret):
            raise PermissionDenied()
        claim = Claim.from_token(token=refresh_token)
        if not claim.user_id:
            raise PermissionDenied()
        principal_id = claim.principal_id
        principal = Principal.objects.get(id=principal_id)
        assert principal.tpa == tpa
        claim1 = Claim(principal_id=principal.id, user_id=principal.user.id, workspace_id=principal.account.workspace.id, account_id=principal.account.id, tpa_id=principal.tpa.id, roles=principal.roles)
        access_token = claim1.to_token(exp_seconds=3600)
        return (refresh_token, access_token)

    def post(self, request):
        client_id = request.data.get('client_id')
        client_secret = request.data.get('client_secret')
        grant_type = request.data.get('grant_type')
        assert grant_type in ['authorization_code', 'refresh_token']
        refresh_token = None
        access_token = None
        if grant_type == 'authorization_code':
            code = request.data.get('code')
            (refresh_token, access_token) = self.process_code(client_id=client_id, client_secret=client_secret, code=code)
        else:
            (refresh_token, access_token) = self.process_refresh_token(client_id=client_id, client_secret=client_secret, refresh_token=refresh_token)
        return Response({ 'refresh_token' : refresh_token, 'access_token' : access_token })
