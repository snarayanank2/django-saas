import logging

from django.contrib.auth.models import User
from rest_framework import serializers

from saas_framework.auth_utils import AuthUtils
from rest_framework.relations import PrimaryKeyRelatedField
from saas_framework.tags.models import Tag
from saas_framework.tags.serializers import TagSerializer
from saas_framework.attachments.models import Attachment
from saas_framework.closed_sets.models import ClosedSet, ClosedSetMember
from saas_framework.workspaces.models import Workspace
from django.contrib.contenttypes.models import ContentType

logger = logging.getLogger(__name__)

class ClosedSetMemberSerializer(serializers.ModelSerializer):
    content_type_id = PrimaryKeyRelatedField(queryset=ContentType.objects.all(), source='content_type')
    object_id = serializers.IntegerField(min_value=0)

    class Meta:
        model = ClosedSetMember
        fields = ['content_type_id', 'object_id']

class ClosedSetSerializer(serializers.ModelSerializer):
    members = ClosedSetMemberSerializer(many=True)

    class Meta:
        model = ClosedSet
        fields = ['id' , 'members']

    def create(self, validated_data):
        members_data = validated_data.pop('members')
        closed_set = ClosedSet.objects.create(**validated_data)
        members = []
        for member_data in members_data:
            (member, created) = ClosedSetMember.objects.get_or_create(**member_data)
            logger.info('added member %s', member)
            members.append(member)
        closed_set.members.set(members)
        return closed_set
    
    def update(self, instance, validated_data):
        members_data = validated_data.pop('members')
        members = []
        closed_set = instance
        for member_data in members_data:
            (member, created) = ClosedSetMember.objects.get_or_create(**member_data)
            members.append(member)
        closed_set.members.set(members)
        return closed_set
