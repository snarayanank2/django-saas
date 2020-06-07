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


class ScheduleViewSet(crud_views.ScheduleViewSet):
    def get_queryset(self):
        return super().get_queryset().filter(
            Exists(WorkspaceSchedule.objects.filter(schedule=OuterRef('pk'), workspace=Workspace.objects.get(id=AuthUtils.get_current_workspace_id())))
        ).order_by('id')

class AccountViewSet(crud_views.AccountViewSet):
    def get_queryset(self):
        return super().get_queryset().filter(workspace=Workspace.objects.get(id=AuthUtils.get_current_workspace_id())).order_by('id')
