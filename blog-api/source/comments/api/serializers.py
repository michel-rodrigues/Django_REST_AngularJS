from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.serializers import (
        HyperlinkedIdentityField,
        ModelSerializer,
        SerializerMethodField,
        ValidationError,
        )

from comments.models import Comment
from accounts.api.serializers import UserDetailSerializer


User = get_user_model()


class CommentCreateSerializer(ModelSerializer):

    user = UserDetailSerializer(read_only=True)
    type = serializers.CharField(required=False, write_only=True)
    slug = serializers.SlugField(write_only=True)
    parent_id = serializers.IntegerField(required=False)

    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            'type',
            'slug',
            'parent_id',
            'timestamp',
            'content',
        ]

    # def __init__(self, *args, **kwargs):
    #     self.model_type = model_type
    #     self.slug = slug
    #     self.parent_obj = None
    #     if parent_id:
    #         parent_qs = Comment.objects.filter(id=parent_id)
    #         if parent_qs.exists() and parent_qs.count() == 1:
    #             self.parent_obj = parent_qs.first()
    #     return super(CommentCreateSerializer, self).__init__(
    #             *args,
    #             **kwargs
    #             )

    def validate(self, data):
        model_type = data.get('type', 'post')
        model_qs = ContentType.objects.filter(model=model_type)
        if not model_qs.exists() or model_qs.count() != 1:
            raise ValidationError("Esse não é um 'content type' válido")
        SomeModel = model_qs.first().model_class()
        slug = data.get('slug')
        obj_qs = SomeModel.objects.filter(slug=slug)
        if not obj_qs.exists() or obj_qs.count() != 1:
            raise ValidationError("Esse não é um 'slug' válido para esse 'content type'")
        parent_id = data.get('parent_id')
        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if not parent_qs.exists() or parent_qs.count() != 1:
                raise ValidationError("Esse não é um 'parent_id' válido para esse 'content type'")
        return data

    def create(self, validated_data):
        content = validated_data.get("content")
        model_type = validated_data.get('type', 'post')
        slug = validated_data.get('slug')
        parent_id = validated_data.get('parent_id')
        parent_obj = None
        if parent_id:
            parent_obj = Comment.objects.get(id=parent_id)
        user = self.context['user']
        comment = Comment.objects.create_by_model_type(
                model_type=model_type,
                slug=slug,
                content=content,
                user=user,
                parent_obj=parent_obj,
                )
        return comment


class CommentListSerializer(ModelSerializer):

    url = HyperlinkedIdentityField(
            view_name='comments-api:thread',
            )

    user = UserDetailSerializer(read_only=True)
    reply_count = SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'url',
            'user',
            # 'content_type',
            # 'object_id',
            # 'parent',
            'timestamp',
            'content',
            'reply_count',
        ]

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0


class CommentChildSerializer(ModelSerializer):

    user = UserDetailSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            'content',
            'timestamp',
        ]


class CommentDetailSerializer(ModelSerializer):

    user = UserDetailSerializer(read_only=True)
    content_object_url = SerializerMethodField()
    replies = SerializerMethodField()
    reply_count = SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            # 'content_type',
            # 'object_id',
            'content_object_url',
            'timestamp',
            'content',
            'reply_count',
            'replies',
        ]
        read_only_fields = [
            # 'content_type',
            # 'object_id',
            'reply_count',
            'replies',
        ]

    def get_content_object_url(self, obj):
        # return obj.content_object.get_absolute_url()
        try:
            return obj.content_object.get_api_url()
        except:
            return None

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0


# class CommentEditSerializer(ModelSerializer):
#
#     class Meta:
#         model = Comment
#         fields = [
#             'id',
#             'timestamp',
#             'content',
#         ]
