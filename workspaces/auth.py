import logging
import threading

logger = logging.getLogger(__name__)

class AuthUtils:
    _storage = threading.local()

    # these utility functions are used by models to automatically determine principal
    @classmethod
    def set_current_claim(cls, claim):
        assert isinstance(claim, dict)
        cls._storage.claim = claim

    @classmethod
    def get_current_principal_id(cls):
        assert hasattr(cls._storage, 'claim')
        return cls._storage.claim['principal_id']

    @classmethod
    def get_current_account_id(cls):
        assert hasattr(cls._storage, 'claim')
        return cls._storage.claim['account_id']

    @classmethod
    def get_current_workspace_id(cls):
        assert hasattr(cls._storage, 'claim')
        return cls._storage.claim['workspace_id']

    @classmethod
    def get_current_user_id(cls):
        assert hasattr(cls._storage, 'claim')
        return cls._storage.claim['user_id']

    @classmethod
    def get_current_roles(cls):
        assert hasattr(cls._storage, 'claim')
        return cls._storage.claim['roles']

    @classmethod
    def get_current_client_application_id(cls):
        assert hasattr(cls._storage, 'claim')
        return cls._storage.claim['client_application_id']

