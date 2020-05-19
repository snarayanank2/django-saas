from rest_framework import serializers
from .models import Workspace, WorkspaceUser, Principal, Comment, Tag, CommentTag
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

class WorkspaceSerializer(serializers.ModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = Workspace
        fields = ['id', 'created_at', 'updated_at', 'name', 'owner']

class WorkspaceUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    workspace = WorkspaceSerializer()

    class Meta:
        model = WorkspaceUser
        fields = ['id', 'created_at', 'updated_at', 'workspace', 'user']

class PrincipalSerializer(serializers.ModelSerializer):
    workspace_user = WorkspaceUserSerializer()

    class Meta:
        model = Principal
        fields = ['id', 'created_at', 'updated_at', 'workspace_user']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class TagRefSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Tag
        fields = ['id']

class CommentSerializer(serializers.ModelSerializer):
    created_by = PrincipalSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'message', 'created_at', 'created_by', 'tags']

class CommentRefSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Comment
        fields = ['id']

class CommentTagSerializer(serializers.ModelSerializer):
    tag = TagRefSerializer()
    comment = CommentRefSerializer()

    class Meta:
        model = CommentTag
        fields = ['tag', 'comment']

    def create(self, validated_data):
        logger.info('validated data = %s', validated_data)
        tag_data = validated_data.pop('tag')
        tag = Tag.objects.get(pk=tag_data['id'])
        comment_data = validated_data.pop('comment')
        comment = Comment.objects.get(pk=comment_data['id'])
        comment_tag = CommentTag.objects.create(**validated_data, comment=comment, tag=tag)
        return comment_tag
