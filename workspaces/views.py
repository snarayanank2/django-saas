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

from .filters import CommentFilter, AccountFilter
from .jwt import JWTUtils
from .models import (Comment, Principal, Tag, Workspace, Account, WorkspaceSchedule, ClientApplication,
                    Attachment)
from django_q.models import Schedule
from .serializers import (CommentSerializer, PrincipalSerializer,
                          TagSerializer, UserSerializer, WorkspaceSerializer,
                          AccountSerializer, AttachmentSerializer, ScheduleSerializer,
                          ClientApplicationSerializer)
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from rest_framework.renderers import JSONRenderer
logger = logging.getLogger(__name__)

class WorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer

    def get_queryset(self):
        logger.info('hooking into get_queryset')
        
        return Workspace.objects.filter(
                Exists(Account.objects.filter(workspace=OuterRef('pk'), user=User.objects.get(id=AuthUtils.get_current_user_id())))
            ).order_by('-created_at')

    def create(self, request):
        res = super().create(request)
        workspace = Workspace.objects.get(id=res.data['id'])
        
        account = Account.objects.create(workspace=workspace, user=User.objects.get(id=AuthUtils.get_current_user_id()), role='admin')
        return res

    @action(detail=True, methods=['post'])
    def auth(self, request, pk=None):
        
        workspace = self.get_object()
        account = Account.objects.get(workspace=workspace, user=User.objects.get(id=AuthUtils.get_current_user_id()))
        (principal, created) = Principal.objects.get_or_create(account=account, client_application=ClientApplication.objects.get(id=AuthUtils.get_current_client_application_id()))
        refresh_token = JWTUtils.get_refresh_token(principal_id=AuthUtils.get_current_principal_id())
        access_token = JWTUtils.get_access_token(principal_id=AuthUtils.get_current_principal_id())
        return Response({ 'refresh_token': refresh_token, 'access_token': access_token })


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
        account = Account.objects.filter(user=user).order_by('-created_at').all()[0]
        # log into the oldest workspace by default
        (principal, created) = Principal.objects.get_or_create(account=account, client_application=client_application)
        refresh_token = JWTUtils.get_refresh_token(principal_id=principal.id)
        access_token = JWTUtils.get_access_token(principal_id=principal.id)
        return Response({ 'refresh_token': refresh_token, 'access_token': access_token })

class BasicAuthSignupView(APIView):
    def post(self, request, format=None):
        """
        Should return access_token, refresh_token
        """
        email = request.data.get('email', None)
        first_name = request.data.get('first_name', None)
        last_name = request.data.get('last_name', None)
        password = request.data.get('password', None) # should confirm password come here?
        if User.objects.filter(username=email).exists():
            raise PermissionDenied()
        user = User.objects.create(first_name=first_name, last_name=last_name, email=email, username=email, password=make_password(password))
        app_name = request.data.get('app_name', 'webapp')
        client_application = ClientApplication.objects.get(name=app_name)
        workspace = Workspace.objects.create(name='Default')
        account = Account.objects.create(user=user, workspace=workspace, role='admin')
        (principal, created) = Principal.objects.get_or_create(workspace=account.workspace, user=account.user, client_application=client_application)
        refresh_token = JWTUtils.get_refresh_token(principal_id=AuthUtils.get_current_principal_id())
        access_token = JWTUtils.get_access_token(principal_id=AuthUtils.get_current_principal_id())
        return Response({ 'refresh_token': refresh_token, 'access_token': access_token })

class RefreshTokenView(APIView):
    def post(self, request, format=None):
        """
        Should return access_token
        """
        claim = JWTUtils.get_claim_from_token(token=request.data.get('refresh_token', None))
        if not claim:
            raise PermissionDenied()
        principal_id = claim['principal_id']
        access_token = JWTUtils.get_access_token(principal_id=principal_id)
        return Response({ 'access_token' : access_token })

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

    def get_object(self):
        logger.info('hooking into get_object')
        
        obj = super().get_object()
        if obj.workspace != Workspace.objects.get(id=AuthUtils.get_current_workspace_id()):
            raise PermissionDenied()
        return obj

    def perform_update(self, serializer):
        logger.info('hooking into update')
        principal = Principal.objects.get(id=AuthUtils.get_current_principal_id())        
        if serializer.instance.workspace != principal.account.workspace:
            raise PermissionDenied()
        updated_by = principal
        serializer.save(updated_by=updated_by)

    def perform_create(self, serializer):
        logger.info('hooking into create')
        principal = Principal.objects.get(id=AuthUtils.get_current_principal_id())
        created_by = principal
        updated_by = principal
        workspace = principal.account.workspace
        serializer.save(created_by=created_by, updated_by=updated_by, workspace=workspace)

    def perform_destroy(self, instance):
        logger.info('hooking into delete')
        principal = Principal.objects.get(id=AuthUtils.get_current_principal_id())        
        if instance.created_by != principal:
            raise PermissionDenied()
        instance.delete()


class AccountViewSet(WorkspaceModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    ordering = 'created_at'

    @action(detail=False, methods=['get'])
    def me(self, request):
        
        account = Account.objects.get(id=AuthUtils.get_current_account_id())
        wus = AccountSerializer(instance=account)
        return Response(wus.data)

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

