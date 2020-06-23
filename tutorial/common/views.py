import logging

from django.contrib.auth.models import User
from django.db.models import Exists, OuterRef
from django.http import HttpResponse
from django.http.response import HttpResponseForbidden
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import (authentication, filters, permissions, status,
                            viewsets)
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from saas_framework.core.accounts.models import Account
from saas_framework.core.accounts.serializers import AccountSerializer
from saas_framework.core.accounts.views import AccountViewSet
from saas_framework.attachments.models import Attachment
from saas_framework.attachments.views import AttachmentViewSet
from saas_framework.comments.views import CommentViewSet
from saas_framework.tags.views import TagViewSet
from saas_framework.core.tpas.views import (AccountThirdPartyAppViewSet,
                                       ThirdPartyAppViewSet)
from saas_framework.core.workspaces.models import Workspace
from saas_framework.core.workspaces.views import WorkspaceViewSet
from saas_framework.core.workspace_membership.mixins import WorkspaceMembershipModelViewSetMixin

logger = logging.getLogger(__name__)

class WorkspaceViewSet(WorkspaceViewSet):
    def get_queryset(self):
        return Workspace.objects.filter(
                Exists(Account.objects.filter(workspace=OuterRef('pk'), user=self.request.claim.user_id))
            ).order_by('-created_at')

    def create(self, request):
        res = super().create(request)
        workspace = Workspace.objects.get(id=res.data['id'])
        account = Account.objects.create(workspace=workspace, user=User.objects.get(id=request.claim.user_id), roles='admin')
        return res


class AccountViewSet(AccountViewSet):
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.claim.user_id).order_by('-created_at')

    @action(detail=False, methods=['get'])
    def me(self, request):
        account = Account.objects.get(id=request.claim.account_id)
        wus = AccountSerializer(instance=account)
        return Response(wus.data)

class ThirdPartyAppViewSet(ThirdPartyAppViewSet):
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.claim.user_id).order_by('-created_at')

    def create(self, request):
        request.data['user_id'] = request.claim.user_id
        return super().create(request)

class AccountThirdPartyAppViewSet(AccountThirdPartyAppViewSet):
    def get_queryset(self):
        return super().get_queryset().filter(account=Account.objects.get(id=request.claim.account_id)).order_by('-created_at')

class AttachmentViewSet(WorkspaceMembershipModelViewSetMixin, AttachmentViewSet):
    pass

class TagViewSet(WorkspaceMembershipModelViewSetMixin, TagViewSet):
    pass

class CommentViewSet(WorkspaceMembershipModelViewSetMixin, CommentViewSet):
    pass
