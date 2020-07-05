import logging

from django.contrib.auth.models import User
from django.db.models import Exists, OuterRef
from saas_framework.roles.models import Role
from saas_framework.workspaces.models import Workspace
from saas_framework.workspaces.views import WorkspaceViewSet

logger = logging.getLogger(__name__)

class WorkspaceViewSet(WorkspaceViewSet):
    def get_queryset(self):
        return Workspace.objects.filter(
                Exists(Role.objects.filter(workspace=OuterRef('pk'), user=self.request.claim.user_id))
            ).order_by('-id')

    def create(self, request):
        res = super().create(request)
        workspace = Workspace.objects.get(id=res.data['id'])
        role = Role.objects.create(workspace=workspace, user=User.objects.get(id=request.claim.user_id), scope='admin,common')
        return res
    
