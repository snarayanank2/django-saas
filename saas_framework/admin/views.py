import logging

from saas_framework.schedules.models import WorkspaceSchedule
from django.db.models.expressions import Exists, OuterRef
from saas_framework.workspaces.models import Workspace
from saas_framework.auth_utils import AuthUtils
from saas_framework.schedules.views import ScheduleViewSet
from saas_framework.accounts.views import AccountViewSet
logger = logging.getLogger(__name__)


class ScheduleViewSet(ScheduleViewSet):
    def get_queryset(self):
        return super().get_queryset().filter(
            Exists(WorkspaceSchedule.objects.filter(schedule=OuterRef('pk'), workspace=Workspace.objects.get(id=AuthUtils.get_current_workspace_id())))
        ).order_by('id')

class AccountViewSet(AccountViewSet):
    def get_queryset(self):
        return super().get_queryset().filter(workspace=Workspace.objects.get(id=AuthUtils.get_current_workspace_id())).order_by('id')
