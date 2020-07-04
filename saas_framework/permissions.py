import inspect
import json
import logging
import re

from rest_framework.permissions import BasePermission

logger = logging.getLogger(__name__)

# Example permissions - please extend to new roles
class RolePolicyPermission(BasePermission):
    # policy is a dict were keys are roles and values are path_regex
    # path_regex should match the specific path that the role is trying to access
    policy = {
        'admin': '/admin/.*',
        'common': '/common/.*'
    }

    # this signifies paths that can accessed by anyone without authentication
    always_allowed = '/auth/.*'

    # paths allowed by any authenticated user
    user_allowed = None

    def is_allowed(self, role, path):
#        logger.info('checking role=%s, path=%s, method=%s', role, path, method)
        if role not in self.policy:
            return False

        role_regex = self.policy[role]
        if re.search(role_regex, path):
            return True

        return False

    def has_permission(self, request, view):
        path = request.get_full_path()
        # logger.info('has permission checking path %s', path)

        if self.always_allowed and re.search(self.always_allowed, path):
            # logger.info('always allowed regex matches')
            return True

        # logger.info('checking path %s against claim.user_id %s', path, request.claim.user_id)

        # if claim has user_id and user_allowed matches then let this call through
        if self.user_allowed and request.claim.user_id and re.search(self.user_allowed, path):
            # logger.info('user allowed regex matches')
            return True

        # logger.info('entering authorization checks')
        scope = request.claim.scope

        if not scope:
            return False

        for role in scope.split(','):
            if self.is_allowed(role, path):
                return True

        return False

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request=request, view=view)
