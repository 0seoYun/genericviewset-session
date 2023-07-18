from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

app_name = "movie"

default_router = routers.SimpleRouter()
default_router.register("movies", MovieViewSet, basename="movies")

comment_router = routers.SimpleRouter()
comment_router.register("comments", CommentViewSet, basename="comments")

movie_comment_router = routers.SimpleRouter()
movie_comment_router.register("comments", MovieCommentViewSet, basename="comments")

tag_router = routers.SimpleRouter()
tag_router.register("tags", TagViewSet, basename="tags")

urlpatterns = [
    path("", include(default_router.urls)),
    path("", include(comment_router.urls)),
    path("movies/<int:movie_id>/", include(movie_comment_router.urls)),
    path("", include(tag_router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
