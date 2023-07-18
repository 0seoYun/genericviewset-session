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

    def get_comments(self, instance):
        serializer = CommentSerializer(instance.comments, many=True)
        return serializer.data

    def get_tag(self, instance):
        tags = instance.tag.all()
        return [tag.name for tag in tags]

    class Meta:
        model = Movie
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "comments"]


# class MovieSerializer(serializers.ModelSerializer):
#     여기에는 read_only = True 아닌 필드만 남기기

#     def get_comments(self, instance):
#         serializer = CommentSerializer(instance.comments, many=True)
#         return serializer.data

#     def get_tag(self, instance):
#         tags = instance.tag.all()
#         return [tag.name for tag in tags]

#     class Meta:
#         model = Movie
#         fields = "__all__"
#         read_only_fields = [여기에 필드 넣어주세요!]


# class MovieListSerializer(serializers.ModelSerializer):
#     comments_cnt 라는 이름의 필드 생성
#     tag = serializers.SerializerMethodField()

#     def get_comments_cnt(self, instance):
#         return 코멘트의 개수

#     def get_tag(self, instance):
#         tags = instance.tag.all()
#         return [tag.name for tag in tags]

#     class Meta:
#           모델은 Movie
#           fields에는 id, name, created_at, updated_at, image, comments_cnt, tag
#           id, created_at, updated_at, commments_cnt 는 읽기만 가능하게


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
        read_only_fields = ["id", "created_at", "updated_at", "comments_cnt"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
