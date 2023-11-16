# Generated by Django 4.2.6 on 2023-11-14 15:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Article",
            fields=[
                (
                    "article_id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="article_id"
                    ),
                ),
                ("author", models.CharField(max_length=200, verbose_name="author")),
                (
                    "category",
                    models.TextField(
                        choices=[
                            ("Sport", "Sport"),
                            ("Finance", "Finance"),
                            ("Politics", "Politics"),
                            ("Health", "Health"),
                        ]
                    ),
                ),
                ("date_time_posted", models.DateTimeField(verbose_name="time_posted")),
                (
                    "date_time_edited",
                    models.DateTimeField(
                        default=models.DateTimeField(verbose_name="time_posted"),
                        verbose_name="time_edited",
                    ),
                ),
                ("contents", models.TextField(verbose_name="content")),
            ],
        ),
        migrations.CreateModel(
            name="Categories",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "category",
                    models.TextField(
                        choices=[
                            ("Sport", "Sport"),
                            ("Finance", "Finance"),
                            ("Politics", "Politics"),
                            ("Health", "Health"),
                        ]
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "comment_id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="comment_id"
                    ),
                ),
                ("date_time_posted", models.DateTimeField(verbose_name="time_posted")),
                (
                    "date_time_edited",
                    models.DateTimeField(
                        default=models.DateTimeField(verbose_name="time_posted"),
                        verbose_name="time_edited",
                    ),
                ),
                ("contents", models.TextField(verbose_name="content")),
            ],
        ),
        migrations.AddField(
            model_name="user",
            name="date_of_birth",
            field=models.DateField(blank=True, null=True, verbose_name="DOB"),
        ),
        migrations.AddField(
            model_name="user",
            name="profile_picture",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="uploads",
                verbose_name="profile_picture",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.CharField(max_length=20, verbose_name="first_name"),
        ),
        migrations.AlterField(
            model_name="user",
            name="last_name",
            field=models.CharField(max_length=20, verbose_name="surname"),
        ),
        migrations.AlterField(
            model_name="user",
            name="password",
            field=models.CharField(max_length=32, verbose_name="password"),
        ),
        migrations.CreateModel(
            name="CommentSection",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "article",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.article"
                    ),
                ),
                ("comments", models.ManyToManyField(to="api.comment")),
            ],
        ),
        migrations.AddField(
            model_name="comment",
            name="posted_by",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="favourite_categories",
            field=models.ManyToManyField(
                to="api.categories", verbose_name="favourites"
            ),
        ),
    ]