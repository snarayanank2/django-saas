import logging

from django.contrib.auth.models import User
from rest_framework import serializers

from rest_framework.relations import PrimaryKeyRelatedField
from saas_framework.tags.models import Tag
from saas_framework.tags.serializers import TagSerializer
from saas_framework.attachments.models import Attachment
from saas_framework.comments.models import Comment
from saas_framework.workspaces.models import Workspace
from django.contrib.contenttypes.models import ContentType
from saas_framework.sharing.models import Sharing

logger = logging.getLogger(__name__)

class SharingSerializer(serializers.ModelSerializer):
    content_type_id = PrimaryKeyRelatedField(queryset=ContentType.objects.all(), source='content_type')
    creator_id = PrimaryKeyRelatedField(queryset=User.objects.all(), source='creator')
    user_id = PrimaryKeyRelatedField(queryset=User.objects.all(), source='user')
    workspace_id = PrimaryKeyRelatedField(queryset=Workspace.objects.all(), source='workspace')

    class Meta:
        model = Sharing
        fields = ['id', 'content_type_id', 'object_id', 'workspace_id', 'user_id', 'creator_id']
