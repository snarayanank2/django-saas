import inspect
import json
import logging
import re

from rest_framework.permissions import BasePermission

logger = logging.getLogger(__name__)

# Example permissions - please extend to new roles
class RolePolicyPermission(BasePermission):
    # policy is a dict were keys are roles and values are list of permissions
    # permission is a dict with the keys: path_regex, read, write
    # path_regex should match the specific path that the role is trying to access
    # read and write are True / False and determine whether the op is allowed or not
    policy = {
        'auditor': [{
            'path_regex' : '.*',
            'read' : True,
            'write' : False
            }],
        'super_admin': [{
            'path_regex' : '.*',
            'read' : True,
            'write' : True
        }]
    }
    always_allowed_regex = '/auth/.*'
    user_allowed_regex = None

    def is_allowed(self, role, path, method):
#        logger.info('checking role=%s, path=%s, method=%s', role, path, method)
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
        logger.info('has permission checking path %s', path)
        method = request.method

        if self.always_allowed_regex and re.search(self.always_allowed_regex, path):
            logger.info('always allowed regex matches')
            return True

        logger.info('checking path %s against claim.user_id %s', path, request.claim.user_id)

        # if claim has user_id and user_allowed_regex matches then let this call through
        if self.user_allowed_regex and request.claim.user_id and re.search(self.user_allowed_regex, path):
            logger.info('user allowed regex matches')
            return True

        logger.info('entering authorization checks')
        scope = request.claim.scope

        if not scope:
            return False

        for role in scope.split(','):
            if self.is_allowed(role, path, method):
                return True

        return False

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request=request, view=view)
