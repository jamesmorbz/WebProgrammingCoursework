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
from django.contrib.sessions.models import Session

def registration_view(request: WSGIRequest):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
        else:
            print(form.error_messages)
    else:
        form = RegistrationForm()
    return render(request, "api/spa/register.html", {"form": form})

def login_view(request: WSGIRequest):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            clean_data: dict = form.cleaned_data
            username = clean_data.get("username")
            password = clean_data.get("password")
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect("/")
    else:
        form = AuthenticationForm()
    return render(request, "api/spa/login.html", {"form": form})

@login_required()
@csrf_exempt
def profile_view(request: WSGIRequest):
    if request.method == "GET":
        try:
            if "sessionid" in request.headers:
                session_key = request.headers.get("sessionid")
                session = Session.objects.get(session_key=session_key)
                uid = session.get_decoded().get('_auth_user_id')
                user = User.objects.get(pk=uid)
            else:
                user: User = request.user
            profile_data = {
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "date_of_birth": user.date_of_birth.isoformat() if user.date_of_birth else None,
                "profile_picture": user.profile_picture.url if user.profile_picture else None,
                "favourite_categories": [category.name for category in user.favourite_categories.all()],
                "date_joined": user.date_joined.isoformat(),
            }
            return JsonResponse(profile_data, safe=False)
        except Exception as e:
            return JsonResponse(
                {
                    "message": f"Unknown error during database operation: {str(e)}",
                },
                status=500,
            )
        
    if request.method == "POST":
        try:
            body: dict = json.loads(request.body)
            if "sessionid" in request.headers:
                session_key = request.headers.get("sessionid")
                session = Session.objects.get(session_key=session_key)
                uid = session.get_decoded().get('_auth_user_id')
                user = User.objects.get(pk=uid)
            else:
                user: User = request.user

            user.first_name = body.get("first_name", user.first_name)
            user.last_name = body.get("last_name", user.last_name)
            user.email = body.get("last_name", user.email)
            user.date_of_birth = body.get("date_of_birth", user.date_of_birth)
            # user.profile_pic = body.get("date_of_birth", user.profile_pic)
            # user.favourites = body.get("date_of_birth", user.favourites)

            user.save()

            return JsonResponse({"message": "Profile updated successfully."})
        except Exception as e:
            return JsonResponse(
                {
                    "message": f"Error updating profile: {str(e)}",
                },
                status=400,
            )

@login_required()
def logout_view(request):
    logout(request)
    return redirect("login")


@login_required()
def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, "api/spa/index.html", {})

@login_required()
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
            body: dict = json.loads(request.body)
            user: User = request.user
        
            Article.objects.create(
                headline=body.get("headline"),
                author=user.username,
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
@login_required()
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

    if request.method == "POST":
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

@login_required()
@csrf_exempt
def comments(request: HttpRequest) -> JsonResponse:
    if request.method == "GET":
        all_comments = []
        for comment in Comment.objects.all():
            date_time_posted_iso = comment.date_time_edited.isoformat()
            date_time_edited_iso = comment.date_time_edited.isoformat()
            doc = {
                "id": comment.comment_id,
                "article_id": comment.article.article_id,
                "article_headline": comment.article.headline,
                "author": comment.posted_by.username,
                "date_time_posted": date_time_posted_iso,
                "date_time_edited": date_time_edited_iso,
                "content": comment.content,
            }
            all_comments.append(doc)
        all_comments = sorted(all_comments, key=lambda x: x['date_time_edited'], reverse=True)
    return JsonResponse(all_comments, safe=False)
    
@login_required()    
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

    if request.method=="GET":
        date_edited_iso = comment.date_time_edited.isoformat()
        date_time_posted_iso = comment.date_time_edited.isoformat()
        doc = {
            "id": comment.comment_id,
            "author": comment.posted_by,
            "date_time_posted": date_time_posted_iso,
            "date_time_edited": date_edited_iso,
            "content": comment.content,
        }
        return JsonResponse(doc)
    
    if request.method== "PUT":
        try:
            body = json.loads(request.body)
            comment.content = body.get("content")
            comment.save()
            return JsonResponse({"message": f"Successfully updated comment"})
        except:
            return JsonResponse(
                {"message": f"ID:{pk} - Incomplete data when updating comment"}
            )
    if request.method== "DELETE":
        try:
            comment.delete()
            return JsonResponse({"message": f"ID:{pk} - Element deleted successfully"})
        except:
            return JsonResponse({"message": f"ID:{pk} - Unable to Delete"}, 500)

@login_required()
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
                date_time_posted_iso = comment.date_time_edited.isoformat()
                date_time_edited_iso = comment.date_time_edited.isoformat()
                doc = {
                    "id": comment.comment_id,
                    "author": comment.posted_by.username,
                    "date_time_posted": date_time_posted_iso,
                    "date_time_edited": date_time_edited_iso,
                    "content": comment.content,
                }
                all_comments.append(doc)
            all_comments = sorted(all_comments, key=lambda x: x['date_time_edited'], reverse=True)
            return JsonResponse(all_comments, safe=False)

    if request.method == "POST":
            try:
                body = json.loads(request.body)
                user: User = request.user
                author_name = user.username            

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
                        "message": "Incomplete data when making comment."
                    },
                    status=400,
                )

@login_required()
@csrf_exempt
def search(request: HttpRequest) -> JsonResponse:
    if request.method == "POST":
        try:
            headline_matches = []
            content_matches = []
            data: dict = json.loads(request.body)
            search_string: str = data.get("search_string").lower()
            for article in Article.objects.all():
                if search_string in article.headline.lower():
                    headline_matches.append(article)
                if search_string in article.content.lower():
                    content_matches.append(article)
            if headline_matches:
                selected_article: Article = random.choice(headline_matches)
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

# @csrf_exempt
# def user(request: HttpRequest) -> JsonResponse:
    # if not request.user.is_authenticated:
    #     return JsonResponse(
    #         {"message": "No user logged in"},
    #         status=404)

    # try:
    #     user = User.objects.get(username=username)
    # except User.DoesNotExist:
    #     return JsonResponse(
    #         {"message": f"User:{username} - Not in Database", "data": str(request)}, status=404
    #     )
    # except Exception as e:
    #     return JsonResponse(
    #         {
    #             "message": f"Username:{username} - Unknown error during database operation",
    #             "data": str(request),
    #         },
    #         status=404,
    #     )
    # match request.method:
    #     case "GET": 
    #         user_dict = {
    #             username
    #             first_name
    #             last_name
    #             date_of_birth
    #             profile_picture
    #             favourite_categories
    #             date_joined
    #         }
    #         return JsonResponse(user_dict)
    #     case "PUT": #maybe throw exception for requests with password field