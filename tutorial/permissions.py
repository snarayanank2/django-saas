import inspect
import json
import logging
import re

from saas_framework.permissions import RolePolicyPermission

logger = logging.getLogger(__name__)

class Permission(RolePolicyPermission):
    # policy is a dict were keys are roles and values are path_regex
    # path_regex should match the specific path that the role is trying to access
    policy = {
        'admin': '/admin/.*',
        'common': '/common/.*'
    }

    # this signifies paths that can accessed by anyone without authentication
    always_allowed = '/(identity|auth|oauth2)/.*'

    # paths allowed by any authenticated user
    user_allowed = '/(workspaces|tpas)/.*'
