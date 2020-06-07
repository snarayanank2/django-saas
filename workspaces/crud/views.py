import logging

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db.models import Exists, OuterRef
from django.http import HttpResponse
from django.http.response import HttpResponseForbidden
from django_filters.rest_framework.backends import DjangoFilterBackend
from django_q.models import Schedule
from rest_framework import (authentication, filters, permissions, status,
                            viewsets)
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.parsers import FileUploadParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from workspaces.auth_utils import AuthUtils
from workspaces.crud.filters import AccountFilter, CommentFilter
from workspaces.jwt import JWTUtils
from workspaces.crud.models import (Account, Attachment, ClientApplication, Comment,
                               Principal, Tag, Workspace, WorkspaceSchedule)
from workspaces.crud.serializers import (AccountSerializer, AttachmentSerializer,
                                    ClientApplicationSerializer,
                                    CommentSerializer, PrincipalSerializer,
                                    ScheduleSerializer, TagSerializer,
                                    UserSerializer, WorkspaceSerializer)

logger = logging.getLogger(__name__)

class WorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    ordering = 'created_at'

class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    ordering = 'created_at'

class ClientApplicationViewSet(viewsets.ModelViewSet):
    queryset = ClientApplication.objects.all()
    serializer_class = ClientApplicationSerializer
    ordering = 'created_at'

class PrincipalViewSet(viewsets.ModelViewSet):
    queryset = Principal.objects.all()
    serializer_class = PrincipalSerializer
    ordering = 'created_at'

class ScheduleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    ordering = 'created_at'

class AttachmentUploadView(APIView):
    parser_class = (FileUploadParser, )

    def post(self, request, *args, **kwargs):
        # logger.info('request %s', request)
        # logger.info('request.Meta %s', request.META)
        attachment_serializer = AttachmentSerializer(data=request.data)
        attachment_serializer.is_valid(raise_exception=True)
        attachment = attachment_serializer.save()
        return Response(attachment_serializer.data, status=status.HTTP_201_CREATED)

class AttachmentDownloadView(APIView):

    def get(self, request, pk, *args, **kwargs):
        attachment = Attachment.objects.get(pk=pk)
        out = attachment.file.open(mode='rb')
        response = HttpResponse(out.read(), content_type=f'{attachment.content_type}')
        response['Content-Disposition'] = f'attachment; filename="{attachment.filename}"'
        return response


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    ordering = 'created_at'

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CommentFilter
    search_fields = ['message']
    ordering_fields = ['created_at']
    ordering = 'created_at'
