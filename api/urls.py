"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse
from .views import (
    main_spa,
    registration_view,
    login_view,
    logout_view,
    profile_view,
    articles,
    articles_pk,
    comments,
    comments_pk,
    comments_articles_pk,
    search,
)

urlpatterns = [
    path("", main_spa),
    path('register/', registration_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path("api/profile/", profile_view, name="profile"),
    path("api/articles/", articles, name="articles"),
    path("api/articles/<int:pk>/", articles_pk, name="articles_pk"),
    path("api/comments/", comments, name="comments"),
    path("api/comments/<int:pk>/", comments_pk, name="comments_pk"),
    path("api/articles/<int:pk>/comments/", comments_articles_pk, name="comments_articles_pk"),
    path("api/search/", search, name="search"),
]
