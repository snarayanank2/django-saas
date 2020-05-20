import logging

from django.contrib.auth.models import User
#from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from .models import (Attachment, Comment, Principal, Tag, Workspace,
                     WorkspaceUser)
from rest_framework.relations import PrimaryKeyRelatedField

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


# Super hack alert: monkey patching the function that disallows nested
# writes and prevents us from doing useful stuff

def raise_errors_on_nested_writes(method_name, serializer, validated_data):
    pass

serializers.raise_errors_on_nested_writes = raise_errors_on_nested_writes

# class BaseSerializer(serializers.ModelSerializer):
    # this serializer does one interesting thing i.e.
    # if an id field is there in the data, it will simply overwrite the rest from
    # the db, if the entry exists

    # def to_internal_value(self, data):
    #     model_class = self.Meta.model
    #     logger.info('to_internal_value type is %s data is %s for model %s', type(data), data, model_class)
    #     # if data has an id, please replace it with whatever data exists in the db
    #     if 'id' in data:
    #         id = data['id']
    #         instance = model_class.objects.get(id=id)
    #         res = self.to_representation(instance)
    #         res['id'] = data['id']
    #         logger.info('modified res = %s', res)
    #         return res
    #     res = super().to_internal_value(data=data)
    #     logger.info('res = %s', res)
    #     return res

    # def create(self, validated_data):
    #     logger.info('called create %s', validated_data)
    #     model_class = self.Meta.model
    #     logger.info('model class is %s', model_class)
    #     if 'id' in validated_data:
    #         id = validated_data['id']
    #         instance = model_class.objects.get(id=id)
    #         logger.info('return instance %s', instance)
    #         return instance
    #     return super().create(validated_data)
    
    # def update(self, instance, validated_data):
    #     logger.info('called update %s', validated_data)
    #     return super().update(validated_data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['id', 'file', 'content_type', 'filename']

class CommentSerializer(serializers.ModelSerializer):
    created_by = PrincipalSerializer(read_only=True)
    tag_ids = PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, write_only=True, source='tags')
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'message', 'created_at', 'created_by', 'tag_ids', 'tags']
