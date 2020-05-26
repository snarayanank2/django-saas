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
            # TODO: only save principal_id and retrieve the principal elsewhere or figure out something
            # better
            principal = JWTUtils.get_principal_from_access_token(access_token=access_token)
            AuthUtils.set_current_principal(principal=principal)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Logic executed before a call to view
        # Gives access to the view itself & arguments
#        logger.info('about to call view %s at path %s with principal %s', view_func, request.path, request.principal)
        if 'basic/signin' not in request.path and AuthUtils.get_current_principal() is None:
            # all other calls, you better have a valid principal attached
            return HttpResponseForbidden('{"message": "missing or invalid token"}', content_type='application/json')
        pass

    def process_exception(self, request, exception):
        # Logic executed if an exception/error occurs in the view
        pass

