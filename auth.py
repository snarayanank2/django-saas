import logging
import threading

logger = logging.getLogger(__name__)

class AuthUtils:
    _storage = threading.local()

    # these utility functions are used by models to automatically determine principal
    @classmethod
    def set_current_principal(cls, principal):
        cls._storage.principal = principal

    @classmethod
    def get_current_principal(cls):
        if (hasattr(cls._storage, 'principal')):
            return cls._storage.principal
        return None
