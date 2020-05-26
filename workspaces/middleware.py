import logging
from .jwt import JWTUtils
from .auth import AuthUtils
from django.http import (
    HttpResponseBadRequest, HttpResponseForbidden
)

logger = logging.getLogger(__name__)

# See https://www.webforefront.com/django/middlewaredjango.html
class AuthMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        if 'HTTP_AUTHORIZATION' in request.META and len(request.META['HTTP_AUTHORIZATION']) > 7:
            access_token = request.META['HTTP_AUTHORIZATION'][7:]
            claim = JWTUtils.get_claim_from_token(token=access_token)
            AuthUtils.set_current_claim(claim=claim)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        return response
    
    def process_exception(self, request, exception):
        # Logic executed if an exception/error occurs in the view
        pass

