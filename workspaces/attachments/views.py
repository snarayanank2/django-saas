import logging


from django.http import HttpResponse
from rest_framework.parsers import FileUploadParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from workspaces.attachments.models import Attachment
from workspaces.attachments.serializers import AttachmentSerializer

logger = logging.getLogger(__name__)

# TODO: api for list of attachments

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
