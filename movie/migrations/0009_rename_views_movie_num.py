# Generated by Django 4.2.1 on 2023-07-19 05:16

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("movie", "0008_rename_num_movie_views"),
    ]

    operations = [
        migrations.RenameField(
            model_name="movie",
            old_name="views",
            new_name="num",
        ),
    ]
