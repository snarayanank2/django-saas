from django.http import JsonResponse
from http import HTTPStatus
import logging

logger = logging.getLogger(__name__)

def error404(request, exception):
    return JsonResponse({'detail' : 'Not found.'}, status=HTTPStatus.NOT_FOUND)

def error500(request):
    return JsonResponse({'detail' : 'Something went wrong. Please try after some time.'}, status=HTTPStatus.INTERNAL_SERVER_ERROR)
