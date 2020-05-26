import logging
import threading

logger = logging.getLogger(__name__)

class AuthUtils:
    _storage = threading.local()

    # these utility functions are used by models to automatically determine principal
    @classmethod
    def set_current_principal(cls, principal):
        assert isinstance(principal, dict)
        cls._storage.principal = principal

    # @classmethod
    # def get_current_principal(cls):
    #     if (hasattr(cls._storage, 'principal')):
    #         return cls._storage.principal
    #     return None

    @classmethod
    def get_current_principal_id(cls):
        assert hasattr(cls._storage, 'principal')
        return cls._storage.principal['id']

    @classmethod
    def get_current_account_id(cls):
        assert hasattr(cls._storage, 'principal')
        return cls._storage.principal['account']['id']

    @classmethod
    def get_current_workspace_id(cls):
        assert hasattr(cls._storage, 'principal')
        return cls._storage.principal['account']['workspace']['id']

    @classmethod
    def get_current_user_id(cls):
        assert hasattr(cls._storage, 'principal')
        return cls._storage.principal['account']['user']['id']

    @classmethod
    def get_current_role(cls):
        assert hasattr(cls._storage, 'principal')
        return cls._storage.principal['account']['role']

    @classmethod
    def get_current_client_application_id(cls):
        assert hasattr(cls._storage, 'principal')
        return cls._storage.principal['client_application']['id']

