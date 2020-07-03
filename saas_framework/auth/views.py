import logging

from rest_framework.exceptions import AuthenticationFailed, ParseError, PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from saas_framework.tokens.token import TokenUtils
from saas_framework.tokens.claim import Claim

logger = logging.getLogger(__name__)


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
