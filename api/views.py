import json
import random

from django.http import HttpResponse, HttpRequest, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth.decorators import login_required
from .models import Article, Comment, User
from datetime import datetime
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt


# def registration_view(request: WSGIRequest):
#     if request.user.is_authenticated:
#         return redirect("profile")
#     if request.method == "POST":
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect("profile")
#         else:
#             print(form.error_messages)
#     else:
#         form = RegistrationForm()
#     return render(request, "api/spa/register.html", {"form": form})


# def login_view(request: WSGIRequest):
#     if request.user.is_authenticated:
#         return redirect("profile")
#     if request.method == "POST":
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get("username")
#             password = form.cleaned_data.get("password")
#             user = authenticate(username=username, password=password)
#             if user:
#                 login(request, user)
#                 return redirect("profile")
#     else:
#         form = AuthenticationForm()
#     return render(request, "api/spa/login.html", {"form": form})


# # @login_required
# def profile_view(request: WSGIRequest):
#     user = request.user
#     username = user.username
#     email = user.email

#     context = {
#         "username": username,
#         "email": email,
#     }
#     return render(request, "api/spa/profile.html", context)


# def logout_view(request):
#     logout(request)
#     return redirect("login")


def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, "api/spa/index.html", {})


@csrf_exempt
def articles(request: HttpRequest) -> JsonResponse:
    if request.method == "GET":
        try:
            all_articles = []
            for article in Article.objects.all():
                date_time_edited_iso = article.date_time_edited.isoformat()
                doc = {
                    "id": article.article_id,
                    "headline": article.headline,
                    "content": article.content,
                    "author": article.author,
                    "category": article.category,
                    "date": date_time_edited_iso,
                }
                all_articles.append(doc)
            return JsonResponse(all_articles, safe=False)
        except:
            return JsonResponse(
                {
                    "message": f"Unknown error during database operation",
                    "data": str(request),
                },
                status=500,
            )

    if request.method == "POST":
        try:
            body = json.loads(request.body)
            Article.objects.create(
                headline=body.get("headline"),
                author=body.get("author"),
                category=body.get("category"),
                content=body.get("content"),
            )
            return JsonResponse({"message": "Article created successfully."})
        except:
            return JsonResponse(
                {
                    "message": "Error creating article."
                },
                status=400,
            )


@csrf_exempt
def articles_pk(request: HttpRequest, pk) -> JsonResponse:
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return JsonResponse(
            {"message": f"ID:{pk} - Not in Database", "data": str(request)}, status=404
        )
    except Exception as e:
        return JsonResponse(
            {
                "message": f"ID:{pk} - Unknown error during database operation",
                "data": str(request),
            },
            status=404,
        )

    if request.method == "GET":
        date_edited_iso = article.date_time_edited.isoformat()
        article_dict = {
            'article_id': article.article_id,
            'headline': article.headline,
            'author': article.author,
            'category': article.category,
            'content': article.content,
            'date': date_edited_iso,
        }
        return JsonResponse(article_dict)

    if request.method == "PUT":
        try:
            body = json.loads(request.body)
            article.headline = body.get("headline")
            article.category = body.get("category")
            article.content = body.get("content")
            article.save()
            print("update article")
            return JsonResponse({"message": f"Successfully updated article"})
        except:
            return JsonResponse(
                {"message": f"ID:{pk} - Incomplete data when updating Article"}
            )

    if request.method == "DELETE":
        try:
            article.delete()
            return JsonResponse({"message": f"ID:{pk} - Element deleted successfully"})
        except:
            return JsonResponse({"message": f"ID:{pk} - Unable to Delete"}, 500)

@csrf_exempt
def comments(request: HttpRequest) -> JsonResponse:
    if request.method == "GET":
        all_comments = []
        for comment in Comment.objects.all():
            doc = {
                "id": comment.comment_id,
                "article_id": comment.article.article_id,
                "article_headline": comment.article.headline,
                "author": comment.posted_by.username,
                "date_time_posted": comment.date_time_posted.isoformat()[:-6],
                "date_time_edited": comment.date_time_edited.isoformat()[:-6],
                "content": comment.content,
            }
            all_comments.append(doc)
        all_comments = sorted(all_comments, key=lambda x: x['date_time_edited'], reverse=True)
    return JsonResponse(all_comments, safe=False)
    
@csrf_exempt
def comments_pk(request: HttpRequest, pk) -> JsonResponse:
    try:
        comment = Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        return JsonResponse(
            {"message": f"ID:{pk} - Not in Database", "data": str(request)}, status=404
        )
    except Exception as e:
        return JsonResponse(
            {
                "message": f"ID:{pk} - Unknown error during database operation - {str(e)}",
                "data": str(request),
            },
            status=404,
        )

    if request.method == "GET":
        doc = {
            "id": comment.comment_id,
            "author": comment.posted_by,
            "date_time_posted": comment.date_time_posted.isoformat()[:-6],
            "date_time_edited": comment.date_time_edited.isoformat()[:-6],
            "content": comment.content,
        }
        return JsonResponse(doc)
    
    if request.method == "PUT":
        try:
            body = json.loads(request.body)
            comment.content = body.get("content")
            comment.save()
            return JsonResponse({"message": f"Successfully updated article"})
        except:
            return JsonResponse(
                {"message": f"ID:{pk} - Incomplete data when updating Article"}
            )

    if request.method == "DELETE":
        try:
            comment.delete()
            return JsonResponse({"message": f"ID:{pk} - Element deleted successfully"})
        except:
            return JsonResponse({"message": f"ID:{pk} - Unable to Delete"}, 500)

@csrf_exempt
def comments_articles_pk(request: HttpRequest, pk) -> JsonResponse:
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return JsonResponse(
            {"message": f"ID:{pk} - Not in Database", "data": str(request)}, status=404
        )
    except Exception as e:
        return JsonResponse(
            {
                "message": f"ID:{pk} - Unknown error during database operation",
                "data": str(request),
            },
            status=404,
        )

    if request.method == "GET":
        all_comments = []
        for comment in Comment.objects.filter(article=article):
            doc = {
                "id": comment.comment_id,
                "author": comment.posted_by.username,
                "date_time_posted": comment.date_time_posted.isoformat()[:-6],
                "date_time_edited": comment.date_time_edited.isoformat()[:-6],
                "content": comment.content,
            }
            all_comments.append(doc)
        all_comments = sorted(all_comments, key=lambda x: x['date_time_edited'], reverse=True)
        return JsonResponse(all_comments, safe=False)

    if request.method == "POST":
        try:
            body = json.loads(request.body)
            author_name = body.get("author")
            user = User.objects.get(username=author_name)
            Comment.objects.create(
                posted_by=user,
                article=article,
                content=body.get("content"),
            )
            return JsonResponse({"message": "Comment created successfully."})
        except:
            return JsonResponse(
                {
                    "message": "Incomplete data. Please provide name, description, price, and is_available."
                },
                status=400,
            )

@csrf_exempt
def search(request: HttpRequest) -> JsonResponse:
    if request.method == "POST":
        try:
            headline_matches = []
            content_matches = []
            search_string = json.loads(request.body).get("search_string").lower()
            for article in Article.objects.all():
                if search_string in article.headline.lower():
                    headline_matches.append(article)
                if search_string in article.content.lower():
                    content_matches.append(article)
            if headline_matches:
                selected_article = random.choice(headline_matches)
                return JsonResponse(
                    {
                        "message": f"Returned randomly selected id based on search string: {search_string} - MATCHED ON HEADLINE",
                        "id": f"{selected_article.article_id}",
                    }
                )
            elif content_matches:
                selected_article = random.choice(content_matches)
                return JsonResponse(
                    {
                        "message": f"Returned randomly selected id based on search string: {search_string} - MATCHED ON CONTENT",
                        "id": f"{selected_article.article_id}",
                    }
                )
            else:
                return JsonResponse(
                    {
                        "message": f"Couldn't find article matching Search String - {search_string}"
                    },
                    status=404,
                )
        except Exception as e:
            return JsonResponse(
                {
                    "message": f"Couldn't find article matching Search String - {search_string}",
                    "error": str(e),
                },
                status=404,
            )
