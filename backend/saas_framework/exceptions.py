import logging
from rest_framework.exceptions import APIException

logger = logging.getLogger(__name__)

class UnAuthorizedException(APIException):
    status_code = 401
    default_detail = 'Unauthorized'
    default_code = 'unauthorized'
