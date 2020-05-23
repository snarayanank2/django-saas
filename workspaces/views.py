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

from .filters import CommentFilter, WorkspaceUserFilter
from .jwt import JWTUtils
from .models import (Comment, Principal, Tag, Workspace, WorkspaceUser, WorkspaceSchedule, ClientApplication,
                    Attachment)
from django_q.models import Schedule
from .serializers import (CommentSerializer, PrincipalSerializer,
                          TagSerializer, UserSerializer, WorkspaceSerializer,
                          WorkspaceUserSerializer, AttachmentSerializer, ScheduleSerializer,
                          ClientApplicationSerializer)
from django.http import HttpResponse

logger = logging.getLogger(__name__)

class WorkspaceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer

    def get_queryset(self):
        logger.info('hooking into get_queryset')
        principal = AuthUtils.get_current_principal()
        return Workspace.objects.filter(
                Exists(WorkspaceUser.objects.filter(workspace=OuterRef('pk'), user=principal.workspace_user.user))
            ).order_by('-created_at')

    @action(detail=True, methods=['post'])
    def auth(self, request, pk=None):
        principal = AuthUtils.get_current_principal()
        workspace = self.get_object()
        workspace_user = WorkspaceUser.objects.get(workspace=workspace, user=principal.workspace_user.user)
        # TODO: catch exception above
        (principal, created) = Principal.objects.get_or_create(workspace_user=workspace_user, client_application=principal.client_application)
        refresh_token = JWTUtils.get_refresh_token(principal_id=principal.id)
        access_token = JWTUtils.get_access_token(principal_id=principal.id)
        return Response({ 'refresh_token': refresh_token, 'access_token': access_token })

    # TODO: add support for creating workspace

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
        principal = AuthUtils.get_current_principal()
        return Schedule.objects.filter(
            Exists(WorkspaceSchedule.objects.filter(schedule=OuterRef('pk'), workspace=principal.workspace_user.workspace))
        ).order_by('id')

class BasicAuthSigninView(APIView):
    def post(self, request, format=None):
        """
        Should return access_token, refresh_token
        """
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        user = authenticate(username=email, password=password)
        if user is None:
            raise AuthenticationFailed()
        app_name = request.data.get('app_name', 'webapp')
        client_application = ClientApplication.objects.get(name=app_name)
        workspace_user = WorkspaceUser.objects.filter(user=user).order_by('-created_at').all()[0]
        (principal, created) = Principal.objects.get_or_create(workspace_user=workspace_user, client_application=client_application)
        refresh_token = JWTUtils.get_refresh_token(principal_id=principal.id)
        access_token = JWTUtils.get_access_token(principal_id=principal.id)
        return Response({ 'refresh_token': refresh_token, 'access_token': access_token })

class BasicAuthSignupView(APIView):
    # TODO: support signup
    pass

class RefreshTokenView(APIView):
    def post(self, request, format=None):
        """
        Should return access_token
        """
        principal = AuthUtils.get_current_principal()
        access_token = JWTUtils.get_access_token(principal_id=principal.id)
        return Response({ 'access_token' : access_token })


class WorkspaceModelViewSet(viewsets.ModelViewSet):
    # all workspace specific viewsets should inherit from this base class. this will 
    # do some magic and add critical information when creating or updating an object
    # and automatically filter out results that are only relevant to current workspace
    def get_queryset(self):
        logger.info('hooking into get_queryset')
        principal = AuthUtils.get_current_principal()
        return super().get_queryset().filter(workspace=principal.workspace_user.workspace).order_by('-created_at')

    def get_object(self):
        logger.info('hooking into get_object')
        principal = AuthUtils.get_current_principal()
        obj = super().get_object()
        if obj.workspace != principal.workspace_user.workspace:
            raise PermissionDenied()
        return obj

    def perform_update(self, serializer):
        logger.info('hooking into update')
        principal = AuthUtils.get_current_principal()
        if serializer.instance.workspace != principal.workspace_user.workspace:
            raise PermissionDenied()
        updated_by = principal
        serializer.save(updated_by=updated_by)

    def perform_create(self, serializer):
        logger.info('hooking into create')
        principal = AuthUtils.get_current_principal()
        created_by = principal
        updated_by = principal
        workspace = principal.workspace_user.workspace
        serializer.save(created_by=created_by, updated_by=updated_by, workspace=workspace)

    def perform_destroy(self, instance):
        logger.info('hooking into delete')
        principal = AuthUtils.get_current_principal()
        if instance.created_by != principal:
            raise PermissionDenied()
        instance.delete()


class TagViewSet(WorkspaceModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    ordering = 'created_at'

class AttachmentUploadView(APIView):
    parser_class = (FileUploadParser, )

    def post(self, request, *args, **kwargs):
        # logger.info('request %s', request)
        # logger.info('request.Meta %s', request.META)
        principal = AuthUtils.get_current_principal()
        created_by = principal
        updated_by = principal
        workspace = principal.workspace_user.workspace
        attachment_serializer = AttachmentSerializer(data=request.data)
        attachment_serializer.is_valid(raise_exception=True)
        attachment = attachment_serializer.save(created_by=created_by, updated_by=updated_by, workspace=workspace)
        return Response(attachment_serializer.data, status=status.HTTP_201_CREATED)

class AttachmentDownloadView(APIView):

    def get(self, request, pk, *args, **kwargs):
        # logger.info('request %s', request)
        # logger.info('request.Meta %s', request.META)
        # logger.info('request.pk %s', pk)
        principal = AuthUtils.get_current_principal()
        attachment = Attachment.objects.get(pk=pk)
        if attachment.workspace != principal.workspace_user.workspace:
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

