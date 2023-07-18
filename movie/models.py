from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


def image_upload_path(instance, filename):
    return f"{instance.pk}/{filename}"


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)


class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    content = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tag = models.ManyToManyField(Tag, blank=True)
    image = models.ImageField(upload_to=image_upload_path, blank=True, null=True)


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(
        Movie,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# class Reaction(models.Model):
#     class ReactionType(models.TextChoices):
#         LIKE = "LIKE", _("LIKE")
#         DISLIKE = "DISLIKE", _("DISLIKE")

#     type = models.CharField(choices=ReactionType.choices, max_length=15)
#     movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reactions")
#     key = models.CharField(max_length=10, blank=True, editable=False)

#     def __str__(self):
#         return f"{self.movie}/{self.key}"
