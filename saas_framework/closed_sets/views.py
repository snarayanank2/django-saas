import logging

from rest_framework import viewsets
from saas_framework.workspaces.models import Workspace
from saas_framework.auth_utils import AuthUtils
from saas_framework.closed_sets.models import ClosedSet
from saas_framework.closed_sets.serializers import ClosedSetSerializer
from django.contrib.contenttypes.models import ContentType
from django.db.models.expressions import Exists, OuterRef
from saas_framework.principals.models import Principal
from django.utils import timezone
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins

logger = logging.getLogger(__name__)

class ClosedSetViewSet(viewsets.ModelViewSet):
    queryset = ClosedSet.objects.all()
    serializer_class = ClosedSetSerializer
    ordering = 'id'

    def list(self, request):
        raise PermissionDenied()
