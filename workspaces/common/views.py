import logging

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Exists, OuterRef
from django.http.response import HttpResponseForbidden
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import authentication, filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from workspaces.auth_utils import AuthUtils

from workspaces.crud.filters import CommentFilter, AccountFilter
from workspaces.jwt import JWTUtils
from workspaces.crud.models import (Comment, Principal, Tag, Workspace, Account, WorkspaceSchedule, ClientApplication,
                    Attachment)
from django_q.models import Schedule
from workspaces.crud.serializers import (CommentSerializer, PrincipalSerializer,
                          TagSerializer, UserSerializer, WorkspaceSerializer,
                          AccountSerializer, AttachmentSerializer, ScheduleSerializer,
                          ClientApplicationSerializer)
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from rest_framework.renderers import JSONRenderer
from workspaces.crud import views as crud_views

logger = logging.getLogger(__name__)

class WorkspaceViewSet(crud_views.WorkspaceViewSet):
    def get_queryset(self):
        logger.info('hooking into get_queryset')        
        return Workspace.objects.filter(
                Exists(Account.objects.filter(workspace=OuterRef('pk'), user=User.objects.get(id=AuthUtils.get_current_user_id())))
            ).order_by('-created_at')

    def create(self, request):
        res = super().create(request)
        workspace = Workspace.objects.get(id=res.data['id'])
        account = Account.objects.create(workspace=workspace, user=User.objects.get(id=AuthUtils.get_current_user_id()), roles='admin')
        return res


class AccountViewSet(crud_views.AccountViewSet):
    def get_queryset(self):
        return Account.objects.filter(user=User.objects.get(id=AuthUtils.get_current_user_id())).order_by('-created_at')

    @action(detail=False, methods=['get'])
    def me(self, request):        
        account = Account.objects.get(id=AuthUtils.get_current_account_id())
        wus = AccountSerializer(instance=account)
        return Response(wus.data)

# Use this mixin to restrict objects to current workspace
class WorkspaceViewMixin:
    def create(self, request):
        request.data['workspace_id'] = AuthUtils.get_current_workspace_id()
        return super().create(request)

    def get_queryset(self):
        return super().get_queryset().filter(workspace=Workspace.objects.get(id=AuthUtils.get_current_workspace_id())).order_by('-created_at')


class AttachmentUploadView(WorkspaceViewMixin, crud_views.AttachmentUploadView):
    pass

class AttachmentDownloadView(crud_views.AttachmentDownloadView):
    # we need to override get here since we are returning http streaming response
    def get(self, request, pk, *args, **kwargs):
        attachment = Attachment.objects.get(pk=pk)
        if attachment.workspace.id != AuthUtils.get_current_workspace_id():
            raise PermissionDenied()
        return super().get(request, pk, *args, **kwargs)

class TagViewSet(WorkspaceViewMixin, crud_views.TagViewSet):
    pass

class CommentViewSet(WorkspaceViewMixin, crud_views.CommentViewSet):
    pass