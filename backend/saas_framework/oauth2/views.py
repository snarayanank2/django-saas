import logging

from rest_framework.exceptions import AuthenticationFailed, ParseError, PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from saas_framework.tokens.token import TokenUtils
from saas_framework.tokens.claim import Claim

logger = logging.getLogger(__name__)

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
        code_challenge = request.query_params.get('code_challenge', None)
        code_challenge_method = request.query_params.get('code_challenge_method', None)
        if code_challenge_method and code_challenge_method != 'S256':
            raise ParseError('Invalid code_challenge_method. Only S256 is supported.')
        code = TokenUtils.oauth2_code(claim=claim, client_id=client_id, scope=scope, code_challenge=code_challenge)
        redirect_uri = redirect_uri + f'?code={code}&state={state}'
        return Response({ 'redirect_uri' : redirect_uri })

class OAuth2Token(APIView):
    def post(self, request):
        client_id = request.data.get('client_id')
        client_secret = request.data.get('client_secret', None)
        grant_type = request.data.get('grant_type')
        code_verifier = request.data.get('code_verifier', None)
        if grant_type == 'authorization_code':
            code = request.data.get('code')
            (refresh_token, access_token) = TokenUtils.oauth2_refresh_token(client_id=client_id, client_secret=client_secret, code=code, code_verifier=code_verifier)
        elif grant_type == 'refresh_token':
            refresh_token = request.data.get('refresh_token')
            (refresh_token, access_token) = TokenUtils.oauth2_access_token(client_id=client_id, client_secret=client_secret, refresh_token=refresh_token, code_verifier=code_verifier)
        else:
            raise ParseError('Invalid grant_type')
        return Response({ 'refresh_token' : refresh_token, 'access_token' : access_token })
