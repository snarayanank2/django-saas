from rest_framework.permissions import BasePermission
import logging
from .auth import AuthUtils
import inspect
import json

logger = logging.getLogger(__name__)

class Permission(BasePermission):

    def has_permission(self, request, view):
        principal = AuthUtils.get_current_principal()
        # logger.info('has_permission called for principal %s', principal)
        # logger.info('info on view %s', inspect.getmembers(view))
        # logger.info('info on request path: %s, data: %s', request.get_full_path(), request.data)
        return True

    def has_object_permission(self, request, view, obj):
        principal = AuthUtils.get_current_principal()
        # logger.info('has_object_permission called %s', principal)
        return True
