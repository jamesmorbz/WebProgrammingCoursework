from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Subjects(models.TextChoices):
      SPORT = "Sport"
      FINANCE = "Finance"
      POLITICS = "Politics"
      HEALTH = "Health"

class Categories(models.Model):
    category = models.TextField(choices=Subjects.choices)

class User(AbstractUser):
    password = models.CharField("password", max_length=32)
    first_name = models.CharField("first_name", max_length=20, editable=True)
    last_name = models.CharField("last_name", max_length=20, editable=True)
    date_of_birth = models.DateField("DOB", editable=True, null=True, blank=True)
    profile_picture = models.ImageField("profile_picture", upload_to="uploads", editable=True, null=True, blank=True)
    favourite_categories = models.ManyToManyField(Categories, verbose_name="favourites", editable=True)

    REQUIRED_FIELDS = ["password"]

class Article(models.Model):
    article_id = models.AutoField("article_id", primary_key=True)
    headline = models.TextField("headline", max_length=200, null=False)
    author = models.CharField("author", max_length=200)
    category = models.TextField(choices=Subjects.choices)
    date_time_posted = models.DateTimeField(auto_now_add=True)
    date_time_edited = models.DateTimeField(auto_now=True, default=date_time_posted)
    contents = models.TextField("content", editable=True)

class Comment(models.Model):
    comment_id = models.AutoField("comment_id", primary_key=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING) # Maybe this should be SET_NULL but I don't know. Need to see what happens during testing
    date_time_posted = models.DateTimeField(auto_now_add=True)
    date_time_edited = models.DateTimeField(auto_now=True, default=date_time_posted)
    contents = models.TextField("content", editable=True)

class CommentSection(models.Model): #One article should be able to have many comments
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    comments = models.ManyToManyField(Comment)