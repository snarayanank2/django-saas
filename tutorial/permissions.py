import inspect
import json
import logging
import re

from saas_framework.permissions import RolePolicyPermission

logger = logging.getLogger(__name__)

# Example permissions - please extend to new roles
class Permission(RolePolicyPermission):
    # policy is a dict were keys are roles and values are list of permissions
    # permission is a dict with the keys: path_regex, read, write
    # path_regex should match the specific path that the role is trying to access
    # read and write are True / False and determine whether the op is allowed or not
    policy = {
        'admin' : [{
            'path_regex' : '/admin/.*',
            'read' : True,
            'write' : True
        }], 
        'auditor': [{
            'path_regex' : '.*',
            'read' : True,
            'write' : False
            }],
        'common': [{
            'path_regex' : '/common/.*',
            'read' : True,
            'write' : True
            }]
    }
    always_allowed_regex = '/auth/.*'
