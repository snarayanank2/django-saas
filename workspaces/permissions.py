from rest_framework.permissions import BasePermission
import logging
from .auth import AuthUtils
import inspect
import json
import re

logger = logging.getLogger(__name__)

class Permission(BasePermission):
    policy = {
        'admin' : [{
            'path_regex' : '.*',
            'read' : True,
            'write' : True
        }]
    }
    always_allowed_regex = '/basic/signin'

    def is_allowed(self, role, path, method):
        logger.info('checking role=%s, path=%s, method=%s', role, path, method)
        rules = self.policy[role]
        for rule in rules:
            regex = rule['path_regex']
            if re.search(regex, path):
                if method in ['GET'] and rule['read']:
                    return True
                if method in ['POST', 'PUT', 'PATCH', 'DELETE'] and rule['write']:
                    return True
                if method in ['OPTIONS']:
                    return True
        return False

    def has_permission(self, request, view):
        path = request.get_full_path()
        method = request.method
        if re.search(self.always_allowed_regex, path):
            return True

        principal = AuthUtils.get_current_principal()
        logger.info('has_permission called for principal %s', principal)
        role = principal.workspace_user.role
        return self.is_allowed(role, path, method)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request=request, view=view)
