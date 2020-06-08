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
from workspaces.accounts.models import Account
from workspaces.accounts.serializers import AccountSerializer
from workspaces.accounts.views import AccountViewSet
from workspaces.attachments.models import Attachment
from workspaces.attachments.views import (AttachmentDownloadView,
                                          AttachmentUploadView)
from workspaces.auth_utils import AuthUtils
from workspaces.comments.views import CommentViewSet
from workspaces.jwt import JWTUtils
from workspaces.tags.views import TagViewSet
from workspaces.workspaces.models import Workspace
from workspaces.workspaces.views import WorkspaceViewSet

logger = logging.getLogger(__name__)

class WorkspaceViewSet(WorkspaceViewSet):
    def get_queryset(self):
        return Workspace.objects.filter(
                Exists(Account.objects.filter(workspace=OuterRef('pk'), user=User.objects.get(id=AuthUtils.get_current_user_id())))
            ).order_by('-created_at')

    def create(self, request):
        res = super().create(request)
        workspace = Workspace.objects.get(id=res.data['id'])
        account = Account.objects.create(workspace=workspace, user=User.objects.get(id=AuthUtils.get_current_user_id()), roles='admin')
        return res


class AccountViewSet(AccountViewSet):
    def get_queryset(self):
        return super().get_queryset().filter(user=User.objects.get(id=AuthUtils.get_current_user_id())).order_by('-created_at')

    @action(detail=False, methods=['get'])
    def me(self, request):        
        account = Account.objects.get(id=AuthUtils.get_current_account_id())
        wus = AccountSerializer(instance=account)
        return Response(wus.data)


class AttachmentUploadView(AttachmentUploadView):
    def post(self, request, *args, **kwargs):
        request.data['workspace_id'] = AuthUtils.get_current_workspace_id()
        logger.info('request.data = %s', request.data)
        return super().post(request)

class AttachmentDownloadView(AttachmentDownloadView):
    # we need to override get here since we are returning http streaming response
    def get(self, request, pk, *args, **kwargs):
        attachment = Attachment.objects.get(pk=pk)
        if attachment.workspace.id != AuthUtils.get_current_workspace_id():
            raise PermissionDenied()
        return super().get(request, pk, *args, **kwargs)

# Use this mixin to restrict objects to current workspace. Ensure that this is the
# first class you inherit from
class WorkspaceViewMixin:
    def create(self, request):
        request.data['workspace_id'] = AuthUtils.get_current_workspace_id()
        logger.info('request.data = %s', request.data)
        return super().create(request)

    def get_queryset(self):
        return super().get_queryset().filter(workspace=Workspace.objects.get(id=AuthUtils.get_current_workspace_id())).order_by('-created_at')

class TagViewSet(WorkspaceViewMixin, TagViewSet):
    pass

class CommentViewSet(WorkspaceViewMixin, CommentViewSet):
    pass
