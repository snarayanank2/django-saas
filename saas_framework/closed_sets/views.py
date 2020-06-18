import logging

from rest_framework import viewsets
from saas_framework.workspaces.models import Workspace
from saas_framework.auth_utils import AuthUtils
from saas_framework.closed_sets.models import (ClosedSet, ClosedSetMembership)
from django.contrib.contenttypes.models import ContentType
from django.db.models.expressions import Exists, OuterRef
from saas_framework.principals.models import Principal
from django.utils import timezone

logger = logging.getLogger(__name__)

class ClosedSetMembershipModelViewSetMixin:
 
    # by default only returns objects in this workspace
    def get_queryset(self):
        closed_set_id = self.request.data.get('closed_set_id', None)
        if not closed_set_id:
            logger.info('no closed_set_id')
            return super().get_queryset()
        else:
            qs = super().get_queryset()
            model = qs.model
            content_type = ContentType.objects.get_for_model(model)
            # given queryset, we need to find content_type
            return super().get_queryset().filter(
                Exists(ClosedSetMembership.objects.filter(object_id=OuterRef('pk'), content_type=content_type, closed_set=closed_set_id)),
            ).order_by('id')

