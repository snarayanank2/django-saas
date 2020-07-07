import logging

from django.contrib.auth.models import User
from django.db.models import Exists, OuterRef
from saas_framework.roles.models import Role
from saas_framework.workspaces.models import Workspace
from saas_framework.workspaces.views import WorkspaceViewSet
from saas_framework.exceptions import UnAuthorizedException

logger = logging.getLogger(__name__)

class WorkspaceViewSet(WorkspaceViewSet):
    def get_queryset(self):
        if not self.request.claim.user_id:
            raise UnAuthorizedException()
        return Workspace.objects.filter(
                Exists(Role.objects.filter(workspace=OuterRef('pk'), user=self.request.claim.user_id))
            ).order_by('-id')

    def create(self, request):
        if not self.request.claim.user_id:
            raise UnAuthorizedException()
        res = super().create(request)
        workspace = Workspace.objects.get(id=res.data['id'])
        role = Role.objects.create(workspace=workspace, user=User.objects.get(id=request.claim.user_id), scope='admin,common')
        return res
    
    def update(self, request, pk=None):
        if not self.request.claim.user_id:
            raise UnAuthorizedException()
        return super().update(request=request, pk=pk)
