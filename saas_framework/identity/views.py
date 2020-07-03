import logging

from rest_framework.exceptions import AuthenticationFailed, ParseError, PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from saas_framework.tokens.token import TokenUtils
from saas_framework.tokens.claim import Claim

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
