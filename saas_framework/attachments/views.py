import logging


from django.http import HttpResponse
from rest_framework.parsers import FileUploadParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from saas_framework.attachments.models import Attachment
from saas_framework.attachments.serializers import AttachmentSerializer
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from saas_framework.closed_sets.views import ClosedSetMembershipModelViewSetMixin

logger = logging.getLogger(__name__)

class AttachmentViewSet(ClosedSetMembershipModelViewSetMixin, viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    ordering = 'created_at'

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        attachment = Attachment.objects.get(pk=pk)
        out = attachment.file.open(mode='rb')
        response = HttpResponse(out.read(), content_type=f'{attachment.content_type}')
        response['Content-Disposition'] = f'attachment; filename="{attachment.filename}"'
        return response
