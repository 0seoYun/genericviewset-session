# Generated by Django 4.2.3 on 2023-07-18 22:55

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("movie", "0003_movie_dislikes_cnt_movie_likes_cnt_reaction"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="movie",
            name="dislikes_cnt",
        ),
        migrations.RemoveField(
            model_name="movie",
            name="likes_cnt",
        ),
    ]