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

class ClosedSetMembershipModelViewSetMixin:
    def get_content_type(self):
        qs = super().get_queryset()
        model = qs.model
        content_type = ContentType.objects.get_for_model(model)
        return content_type

    # by default only returns objects in this workspace
    def get_queryset(self):
        closed_set_id = self.request.query_params.get('closed_set_id', None)
        if not closed_set_id:
            logger.info('no closed_set_id')
            return super().get_queryset()
        else:
            logger.info('yes closed_set_id')
            content_type = self.get_content_type()
            return super().get_queryset().filter(
                Exists(ClosedSet.objects.filter(members__object_id=OuterRef('pk'), members__content_type=content_type, id=closed_set_id)),
            ).order_by('id')

    @action(detail=False, methods=['get'])
    def content_type(self, request):
        content_type = self.get_content_type()
        return Response({ 'content_type_id' : content_type.id })

