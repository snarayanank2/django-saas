import logging

from saas_framework.schedules.models import WorkspaceSchedule
from django.db.models.expressions import Exists, OuterRef
from saas_framework.workspaces.models import Workspace
from saas_framework.auth_utils import AuthUtils
from saas_framework.schedules.views import ScheduleViewSet
from saas_framework.accounts.views import AccountViewSet
from saas_framework.users.views import UserViewSet
from saas_framework.tpas.views import ThirdPartyAppViewSet
from saas_framework.accounts.models import Account
from django.contrib.auth.models import User
from rest_framework.exceptions import PermissionDenied
from saas_framework.tpas.models import AccountThirdPartyApp

logger = logging.getLogger(__name__)

class UserViewSet(UserViewSet):
    def get_queryset(self):
        return super().get_queryset().filter(
                Exists(Account.objects.filter(user=OuterRef('pk'), workspace=AuthUtils.get_current_workspace_id()))
            ).order_by('-id')

class ScheduleViewSet(ScheduleViewSet):
    def get_queryset(self):
        return super().get_queryset().filter(
            Exists(WorkspaceSchedule.objects.filter(schedule=OuterRef('pk'), workspace=AuthUtils.get_current_workspace_id()))
        ).order_by('id')

class AccountViewSet(AccountViewSet):
    def get_queryset(self):
        return super().get_queryset().filter(workspace=AuthUtils.get_current_workspace_id()).order_by('id')

class ThirdPartyAppViewSet(ThirdPartyAppViewSet):
    def get_queryset(self):
        return super().get_queryset().filter(
            Exists(AccountThirdPartyApp.objects.filter(tpa=OuterRef('pk'), workspace=AuthUtils.get_current_workspace_id()))
            ).order_by('-created_at')

    def create(self, request):
        # admins cannot create
        raise PermissionDenied()