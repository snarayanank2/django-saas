import logging
from saas_framework.tpas.models import AccountThirdPartyApp, ThirdPartyApp
from saas_framework.tpas.serializers import AccountThirdPartyAppSerializer, ThirdPartyAppSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from saas_framework.jwt import JWTUtils
from saas_framework.accounts.models import Account
from rest_framework.exceptions import PermissionDenied
from saas_framework.workspaces.models import Workspace
from django.contrib.auth.hashers import make_password
from saas_framework.principals.models import Principal
from rest_framework.views import APIView

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
        claim = {
            'atpa_id' : atpa.id
        }
        code = JWTUtils.get_token_from_claim(claim=claim, exp_seconds=3600)
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
        claim = JWTUtils.get_claim_from_token(token=code)
        logger.info('claim = %s', claim)
        atpa_id = claim['atpa_id']
        atpa = AccountThirdPartyApp.objects.get(id=atpa_id)
        assert tpa == atpa.tpa
        (principal, created) = Principal.objects.get_or_create(account=atpa.account, tpa=atpa.tpa, roles=atpa.roles)
        refresh_token = JWTUtils.get_refresh_token(principal_id=principal.id)
        access_token = JWTUtils.get_access_token(principal_id=principal.id)
        return (refresh_token, access_token)

    def process_refresh_token(self, client_id, client_secret, refresh_token):
        tpa = ThirdPartyApp.objects.get(id=client_id)
        if tpa.secret != make_password(client_secret):
            raise PermissionDenied()
        claim = JWTUtils.get_claim_from_token(token=refresh_token)
        if not claim:
            raise PermissionDenied()
        principal_id = claim['principal_id']
        principal = Principal.objects.get(id=principal_id)
        assert principal.tpa == tpa
        access_token = JWTUtils.get_access_token(principal_id=principal_id)
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
