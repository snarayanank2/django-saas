import logging

from django.contrib.auth.models import User
from rest_framework import viewsets
from workspaces.users.serializers import UserSerializer

logger = logging.getLogger(__name__)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    ordering = 'created_at'

