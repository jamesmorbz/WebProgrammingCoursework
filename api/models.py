from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CATEGORIES(models.TextChoices): #Enum class of news catergories
      SPORT = "Sport"
      FINANCE = "Finance"
      POLITICS = "Politics"
      HEALTH = "Health"

class User(AbstractUser):
    EMAIL_FIELD = models.EmailField("Email", editable=True)
    USERNAME_FIELD = models.CharField("Username", max_length=200, primary_key=True)
    password = models.CharField("Password", max_length=200) #This may have to change when authentication is implemented

    first_name = models.CharField("Name", max_length=200)
    last_name = models.CharField("Surname", max_length=200)
    date_of_birth = models.DateField("D.O.B.", editable=True)
    profile_picture = models.ImageField("Profile Picture", upload_to="uploads", editable=True)
    favourite_categories = models.ManyToManyField("Favourite Categories", choices=CATEGORIES) #Trying to find a way to make this field and multi select

    REQUIRED_FIELDS = ["EMAIL_FIELD", "USERNAME_FIELD", "password", "date_of_birth", "profile_picture"]

class Article(models.Model):
    article_id = models.AutoField("Article ID", primary_key=True)
    author = models.CharField("Author", max_length=200)
    category = models.CharField(choices=CATEGORIES, max_length=8)
    date_time_posted = models.DateTimeField("Date/Time Posted")
    date_time_edited = models.DateTimeField("Date/Time Edited", default=date_time_posted) #Should update whenever an edit to an article is saved
    contents = models.TextField("Contents", editable=True)

class Comment(models.Model):
    comment_id = models.AutoField("Comment ID", primary_key=True)
    posted_by = models.ForeignKey("User", on_delete=models.SET_NULL)
    date_time_posted = models.DateTimeField("Date/Time Posted")
    date_time_edited = models.DateTimeField("Date/Time Edited", default=date_time_posted) #Should update whenever an edit to a comment is saved
    contents = models.TextField("Contents", editable=True)

class CommentSection(models.Model): #One article should be able to have many comments
    article = models.ForeignKey(Article)
    comments = models.ManyToManyField(Comment)