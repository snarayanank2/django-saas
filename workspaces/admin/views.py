import logging

from workspaces.schedules.models import WorkspaceSchedule
from django.db.models.expressions import Exists, OuterRef
from workspaces.workspaces.models import Workspace
from workspaces.auth_utils import AuthUtils
from workspaces.schedules.views import ScheduleViewSet
from workspaces.accounts.views import AccountViewSet
logger = logging.getLogger(__name__)


class ScheduleViewSet(ScheduleViewSet):
    def get_queryset(self):
        return super().get_queryset().filter(
            Exists(WorkspaceSchedule.objects.filter(schedule=OuterRef('pk'), workspace=Workspace.objects.get(id=AuthUtils.get_current_workspace_id())))
        ).order_by('id')

class AccountViewSet(AccountViewSet):
    def get_queryset(self):
        return super().get_queryset().filter(workspace=Workspace.objects.get(id=AuthUtils.get_current_workspace_id())).order_by('id')
