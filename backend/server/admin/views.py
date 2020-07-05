import logging

from django.contrib.auth.models import User
from django.db.models.expressions import Exists, OuterRef
from rest_framework.exceptions import PermissionDenied

from saas_framework.roles.models import Role
from saas_framework.roles.views import RoleViewSet
from saas_framework.schedules.views import ScheduleViewSet
from saas_framework.sharing.mixins import SharingModelViewSetMixin
from saas_framework.tpas.models import ThirdPartyAppInstall
from saas_framework.tpas.views import ThirdPartyAppViewSet
from saas_framework.users.views import UserViewSet
from saas_framework.workspaces.models import Workspace

logger = logging.getLogger(__name__)

class UserViewSet(UserViewSet):
    def get_queryset(self):
        return super().get_queryset().filter(
                Exists(Role.objects.filter(user=OuterRef('pk'), workspace=self.request.claim.workspace_id))
            ).order_by('-id')

class RoleViewSet(RoleViewSet):
    def get_queryset(self):
        return super().get_queryset().filter(workspace=self.request.claim.workspace_id).order_by('id')

class ThirdPartyAppViewSet(ThirdPartyAppViewSet):
    def get_queryset(self):
        return super().get_queryset().filter(
            Exists(ThirdPartyAppInstall.objects.filter(tpa=OuterRef('pk'), workspace=self.request.claim.workspace_id))
            ).order_by('-created_at')

    def create(self, request):
        # admins cannot create
        raise PermissionDenied()

class ScheduleViewSet(SharingModelViewSetMixin, ScheduleViewSet):
    pass
