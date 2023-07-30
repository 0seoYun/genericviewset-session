from rest_framework import serializers
from .models import *


class CommentSerializer(serializers.ModelSerializer):
    movie = serializers.SerializerMethodField()

    def get_movie(self, instance):
        return instance.movie.name

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["movie"]


class MovieSerializer(serializers.ModelSerializer):
    tag = serializers.SerializerMethodField()
    image = serializers.ImageField(use_url=True, required=False)
    comments = serializers.SerializerMethodField()

    # 단, comments는 read_only=True이지만, SerializerMethodField이므로 유지!
    def get_comments(self, instance):
        serializer = CommentSerializer(instance.comments, many=True)
        return serializer.data

    def get_tag(self, instance):
        tags = instance.tag.all()
        return [tag.name for tag in tags]

    class Meta:
        model = Movie
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "comments",
            "num",
        ]


class MovieListSerializer(serializers.ModelSerializer):
    comments_cnt = serializers.SerializerMethodField()
    tag = serializers.SerializerMethodField()

    def get_comments_cnt(self, instance):
        return instance.comments.count()

    def get_tag(self, instance):
        tags = instance.tag.all()
        return [tag.name for tag in tags]

    class Meta:
        model = Movie
        fields = [
            "id",
            "name",
            "created_at",
            "updated_at",
            "image",
            "comments_cnt",
            "tag",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "comments_cnt",
        ]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
