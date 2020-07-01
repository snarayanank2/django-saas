import logging

from rest_framework.exceptions import AuthenticationFailed, ParseError, PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from saas_framework.core.auth.token import TokenUtils
from saas_framework.core.auth.claim import Claim

logger = logging.getLogger(__name__)

class BasicAuthSigninView(APIView):
    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        app_name = request.data.get('app_name', 'webapp')
        (refresh_token, access_token) = TokenUtils.signin(email=email, password=password, app_name=app_name)
        return Response({ 'refresh_token': refresh_token, 'access_token': access_token })

class BasicAuthSignupView(APIView):
    def post(self, request):
        email = request.data.get('email', None)
        first_name = request.data.get('first_name', None)
        last_name = request.data.get('last_name', None)
        password = request.data.get('password', None) # TODO: should confirm password come here?
        app_name = request.data.get('app_name', 'webapp')
        (refresh_token, access_token) = TokenUtils.signup(email=email, first_name=first_name, last_name=last_name, password=password, app_name=app_name)
        return Response({ 'refresh_token': refresh_token, 'access_token': access_token })

class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token', None)
        access_token = TokenUtils.access_token(refresh_token=refresh_token)
        return Response({ 'access_token' : access_token })

class SwitchWorkspaceView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        workspace_id = request.data.get('workspace_id')
        (refresh_token, access_token) = TokenUtils.switch_workspace(refresh_token=refresh_token, workspace_id=workspace_id)
        return Response({ 'refresh_token': refresh_token, 'access_token': access_token })

class JwtDecode(APIView):
    def post(self, request):
        jwt = request.data['jwt']
        claim = Claim.from_token(token=jwt)
        return Response({ 'claim' : claim.__dict__ })

class OAuth2Authorize(APIView):
    def get(self, request):
        claim = request.claim
        client_id = request.query_params.get('client_id')
        response_type = request.query_params.get('response_type')
        if response_type not in ['code']:
            raise ParseError('Invalid response_type')
        state = request.query_params.get('state', '')
        redirect_uri = request.query_params.get('redirect_uri')
        scope = request.query_params.get('scope')
        code = TokenUtils.oauth2_code(claim=claim, client_id=client_id, scope=scope)
        redirect_uri = redirect_uri + f'?code={code}&state={state}'
        return Response({ 'redirect_uri' : redirect_uri })

class OAuth2Token(APIView):
    def post(self, request):
        client_id = request.data.get('client_id')
        client_secret = request.data.get('client_secret')
        grant_type = request.data.get('grant_type')
        if grant_type == 'authorization_code':
            code = request.data.get('code')
            (refresh_token, access_token) = TokenUtils.oauth2_refresh_token(client_id=client_id, client_secret=client_secret, code=code)
        elif grant_type == 'refresh_token':
            refresh_token = request.data.get('refresh_token')
            (refresh_token, access_token) = TokenUtils.oauth2_access_token(client_id=client_id, client_secret=client_secret, refresh_token=refresh_token)
        else:
            raise ParseError('Invalid grant_type')
        return Response({ 'refresh_token' : refresh_token, 'access_token' : access_token })
