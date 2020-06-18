import logging

from rest_framework import viewsets
from saas_framework.workspaces.models import Workspace
from saas_framework.auth_utils import AuthUtils
from saas_framework.closed_sets.models import (ClosedSet, ClosedSetMembership)
from django.contrib.contenttypes.models import ContentType
from django.db.models.expressions import Exists, OuterRef
from saas_framework.principals.models import Principal
from django.utils import timezone
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action
from rest_framework.response import Response

logger = logging.getLogger(__name__)

# TODO: this is incomplete - need to figure out a way to do this properly

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
            content_type = self.get_content_type()
            # given queryset, we need to find content_type
            return super().get_queryset().filter(
                Exists(ClosedSetMembership.objects.filter(object_id=OuterRef('pk'), content_type=content_type, closed_set=closed_set_id)),
            ).order_by('id')

    # @action(detail=False, methods=['get'])
    # def content_type(self, request):
    #     content_type = self.get_content_type()
    #     return Response({ 'id' : content_type.id })

    @action(detail=False, methods=['post'])
    def closed_sets(self, request):
        ids = request.data.get('ids')
        content_type = self.get_content_type()
        closed_set = ClosedSet.objects.create()
        for id in ids:
            ClosedSetMembership.objects.create(content_type=content_type, object_id=id, closed_set=closed_set)
        return Response({ 'id' : closed_set.id })
