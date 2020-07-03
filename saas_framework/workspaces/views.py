import logging

from rest_framework import viewsets
from saas_framework.workspaces.models import Workspace
from saas_framework.workspaces.serializers import WorkspaceSerializer
from saas_framework.tokens.token import TokenUtils
from rest_framework.decorators import action
from rest_framework.response import Response

logger = logging.getLogger(__name__)

class WorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    ordering = 'created_at'

    @action(detail=True, methods=['post'])
    def switch(self, request, pk=None):
        workspace_id = pk
        user_id = request.claim.user_id
        (refresh_token, access_token) = TokenUtils.switch_workspace(user_id=user_id, workspace_id=workspace_id)
        return Response({ 'refresh_token': refresh_token, 'access_token': access_token })

