import logging

from django.contrib.auth.models import User
from django.db.models import Exists, OuterRef
from rest_framework import (authentication, filters, permissions, status,
                            viewsets)
from rest_framework.response import Response

from saas_framework.tpas.views import (ThirdPartyAppViewSet)
from saas_framework.workspaces.models import Workspace

logger = logging.getLogger(__name__)

class ThirdPartyAppViewSet(ThirdPartyAppViewSet):
    def get_queryset(self):
        return super().get_queryset().filter(creator=self.request.claim.user_id).order_by('-id')

    def create(self, request):
        # TODO: use perform_create
        _mutable = request.data._mutable
        request.data._mutable = True
        request.data['creator_id'] = request.claim.user_id
        request.data._mutable = _mutable
        return super().create(request)

