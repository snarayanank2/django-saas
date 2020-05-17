from rest_framework import viewsets
from rest_framework import permissions
from .models import Workspace, WorkspaceUser, Principal, Comment
from .serializers import UserSerializer, WorkspaceSerializer, WorkspaceUserSerializer, PrincipalSerializer, CommentSerializer
from django.contrib.auth.models import User
from .filters import WorkspaceUserFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
import logging
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from .jwt import JWTUtils
from rest_framework.decorators import action
from django.http.response import HttpResponseForbidden
from workspaces.auth import AuthUtils
from django.db.models import Exists, OuterRef

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

    # TODO: add support for creating workspace

# class PrincipalViewSet(viewsets.ModelViewSet):
#     queryset = Principal.objects.all()
#     serializer_class = PrincipalSerializer

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
        workspace_user = WorkspaceUser.objects.filter(user=user).order_by('-created_at').all()[0]
        (principal, created) = Principal.objects.get_or_create(workspace_user=workspace_user)
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

class WorkspaceUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WorkspaceUser.objects.all()
    serializer_class = WorkspaceUserSerializer

    def get_queryset(self):
        logger.info('hooking into get_queryset')
        principal = AuthUtils.get_current_principal()
        return WorkspaceUser.objects.filter(user=principal.workspace_user.user).order_by('-created_at')

    @action(detail=True, methods=['post'])
    def auth(self, request, pk=None):
        principal = AuthUtils.get_current_principal()
        workspace_user = self.get_object()
        if principal.workspace_user.user != workspace_user.user:
            raise PermissionDenied()
        (principal, created) = Principal.objects.get_or_create(workspace_user=workspace_user)
        refresh_token = JWTUtils.get_refresh_token(principal_id=principal.id)
        access_token = JWTUtils.get_access_token(principal_id=principal.id)
        return Response({ 'refresh_token': refresh_token, 'access_token': access_token })


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


class CommentViewSet(WorkspaceModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
