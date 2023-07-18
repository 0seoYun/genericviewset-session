from rest_framework import viewsets, mixins
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import action
from django.utils import timezone

from .models import Movie, Comment, Tag
from .serializers import (
    MovieSerializer,
    CommentSerializer,
    TagSerializer,
    MovieListSerializer,
)


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    # queryset = Movie.objects.filter(created_at__gte=timezone.now())

    def get_serializer_class(self):
        if self.action == "list":
            return MovieListSerializer
        return MovieSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        movie = serializer.instance
        self.handle_tags(movie)

        return Response(serializer.data)

    def perform_update(self, serializer):
        movie = serializer.save()
        movie.tag.clear()
        self.handle_tags(movie)

    def handle_tags(self, movie):
        words = movie.content.split(" ")
        tag_list = []
        for w in words:
            if w[0] == "#":
                tag_list.append(w[1:])

        for t in tag_list:
            tag, created = Tag.objects.get_or_create(name=t)
            movie.tag.add(tag)

        movie.save()

    def get_permissions(self):
        if self.action in ["update", "destroy"]:
            return [IsAdminUser()]
        return []

    @action(methods=["GET"], detail=False)
    def recommend(self, request):
        ran_movie = self.get_queryset().order_by("?")[:1]
        ran_movie_serializer = MovieListSerializer(
            ran_movie, many=True, context={"request": request}
        )
        return Response(ran_movie_serializer.data)


class CommentViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ["update", "destroy"]:
            return [IsOwnerOrReadOnly()]
        return []

    # def 동적으로 권한 설정 가능 메서드:
    #   만약 액션이 update, destroy라면:
    #       IsOwnerOrReadOnly 권한 클래스의 인스턴스를 요소로 갖는 리스트 반환
    #   그 외에는 빈 리스트 반환


class MovieCommentViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin
):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        movie = self.kwargs.get("movie_id")
        queryset = Comment.objects.filter(movie_id=movie)
        return queryset

    def create(self, request, movie_id=None):
        movie = get_object_or_404(Movie, id=movie_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(movie=movie)
        return Response(serializer.data)


class TagViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = "name"
    lookup_url_kwarg = "tag_name"

    def retrieve(self, request, *args, **kwargs):
        tag_name = kwargs.get("tag_name")
        tag = self.get_object()
        tag = get_object_or_404(Tag, name=tag_name)
        movies = Movie.objects.filter(tag=tag)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
