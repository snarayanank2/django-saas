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
from workspaces.auth import AuthUtils

from workspaces.filters import CommentFilter, AccountFilter
from workspaces.jwt import JWTUtils
from workspaces.models import (Comment, Principal, Tag, Workspace, Account, WorkspaceSchedule, ClientApplication,
                    Attachment)
from django_q.models import Schedule
from workspaces.serializers import (CommentSerializer, PrincipalSerializer,
                          TagSerializer, UserSerializer, WorkspaceSerializer,
                          AccountSerializer, AttachmentSerializer, ScheduleSerializer,
                          ClientApplicationSerializer)
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from rest_framework.renderers import JSONRenderer
logger = logging.getLogger(__name__)


class ClientApplicationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ClientApplication.objects.all()
    serializer_class = ClientApplicationSerializer


# class PrincipalViewSet(viewsets.ModelViewSet):
#     queryset = Principal.objects.all()
#     serializer_class = PrincipalSerializer

class ScheduleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        
        return Schedule.objects.filter(
            Exists(WorkspaceSchedule.objects.filter(schedule=OuterRef('pk'), workspace=Workspace.objects.get(id=AuthUtils.get_current_workspace_id())))
        ).order_by('id')


class WorkspaceModelViewSet(viewsets.ModelViewSet):
    # all workspace specific viewsets should inherit from this base class. this will 
    # do some magic and add critical information when creating or updating an object
    # and automatically filter out results that are only relevant to current workspace
    def get_queryset(self):
        logger.info('hooking into get_queryset')
        return super().get_queryset().filter(workspace=Workspace.objects.get(id=AuthUtils.get_current_workspace_id())).order_by('-created_at')

class AccountViewSet(WorkspaceModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    ordering = 'created_at'

class TagViewSet(WorkspaceModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    ordering = 'created_at'

class AttachmentUploadView(APIView):
    parser_class = (FileUploadParser, )

    def post(self, request, *args, **kwargs):
        # logger.info('request %s', request)
        # logger.info('request.Meta %s', request.META)
        principal = Principal.objects.get(id=AuthUtils.get_current_principal_id())        
        created_by = principal
        updated_by = principal
        workspace = Workspace.objects.get(id=AuthUtils.get_current_workspace_id())
        attachment_serializer = AttachmentSerializer(data=request.data)
        attachment_serializer.is_valid(raise_exception=True)
        attachment = attachment_serializer.save(created_by=created_by, updated_by=updated_by, workspace=workspace)
        return Response(attachment_serializer.data, status=status.HTTP_201_CREATED)

class AttachmentDownloadView(APIView):

    def get(self, request, pk, *args, **kwargs):
        # logger.info('request %s', request)
        # logger.info('request.Meta %s', request.META)
        # logger.info('request.pk %s', pk)
        
        attachment = Attachment.objects.get(pk=pk)
        if attachment.workspace != Workspace.objects.get(id=AuthUtils.get_current_workspace_id()):
            raise PermissionDenied()
        out = attachment.file.open(mode='rb')
        response = HttpResponse(out.read(), content_type=f'{attachment.content_type}')
        response['Content-Disposition'] = f'attachment; filename="{attachment.filename}"'
        return response

class CommentViewSet(WorkspaceModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CommentFilter
    search_fields = ['message']
    ordering_fields = ['created_at']
    ordering = 'created_at'

