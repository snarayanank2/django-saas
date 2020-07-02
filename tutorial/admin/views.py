import logging

from django.db.models.expressions import Exists, OuterRef
from saas_framework.workspaces.models import Workspace
from saas_framework.schedules.views import ScheduleViewSet
from saas_framework.accounts.views import AccountViewSet
from saas_framework.users.views import UserViewSet
from saas_framework.tpas.views import ThirdPartyAppViewSet
from saas_framework.accounts.models import Account
from django.contrib.auth.models import User
from rest_framework.exceptions import PermissionDenied
from saas_framework.tpas.models import AccountThirdPartyApp
from saas_framework.sharing.mixins import SharingModelViewSetMixin

logger = logging.getLogger(__name__)

class UserViewSet(UserViewSet):
    def get_queryset(self):
        return super().get_queryset().filter(
                Exists(Account.objects.filter(user=OuterRef('pk'), workspace=self.request.claim.workspace_id))
            ).order_by('-id')

class AccountViewSet(AccountViewSet):
    def get_queryset(self):
        return super().get_queryset().filter(workspace=self.request.claim.workspace_id).order_by('id')

class ThirdPartyAppViewSet(ThirdPartyAppViewSet):
    def get_queryset(self):
        return super().get_queryset().filter(
            Exists(AccountThirdPartyApp.objects.filter(tpa=OuterRef('pk'), workspace=self.request.claim.workspace_id))
            ).order_by('-created_at')

    def create(self, request):
        # admins cannot create
        raise PermissionDenied()

class ScheduleViewSet(SharingModelViewSetMixin, ScheduleViewSet):
    pass
