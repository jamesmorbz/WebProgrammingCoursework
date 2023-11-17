import json
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth.decorators import login_required
from .models import Article, Comment
from datetime import datetime
from django.forms.models import model_to_dict

def response(message: str, code: int) -> HttpResponse:
    return HttpResponse({'message': message, 'code': code})

def registration_view(request: WSGIRequest):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
        else:
            print(form.error_messages)
    else:
        form = RegistrationForm()
    return render(request, 'api/spa/register.html', {'form': form})

def login_view(request: WSGIRequest):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'api/spa/login.html', {'form': form})

@login_required 
def profile_view(request: WSGIRequest):
    user = request.user 
    username = user.username
    email = user.email

    context = {
        'username': username,
        'email': email,
    }
    return render(request, 'api/spa/profile.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')

def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})

def get_articles(request: HttpRequest) -> JsonResponse:
    if request.method == 'GET':
        try:
            all_articles = model_to_dict(Article.objects.all())
            return response('Article created successfully', 200)
        except:
            return response('Error parsing new article object, check request again', 400)
    
    if request.method == 'POST':
        try:
            body: dict = json.loads(request.body)
            new_article = Article(
                headline=body.get('headline'),
                author=body.get('author'),
                category=body.get('category'),
                date_time_posted=datetime.now(),
                date_time_edited=datetime.now(),
                contents=body.get('contents')
            )
            new_article.save()
            return response('Article created successfully', 200)
        except:
            return response('Error parsing new article object, check request again', 400)
        
    return JsonResponse(all_articles)

def article(request: HttpRequest, pk) -> JsonResponse:
    try:
        article = Article.objects.get(pk=pk)
        data = json.loads(request.body)
    except Exception as e:
        return JsonResponse({"message":f"ID:{pk} Not in Database or Bad Data Sent in Request", "data": str(request.body)}, status=404)
    
    if request.method == 'GET':
        try:
            body: dict = json.loads(request.body)
            article: Article = Article.objects.filter(article_id=body.get('article_id'))
            if (article is None): #If get returns empty object
                return response('Article not found', 404)
            else:
                return HttpResponse({'article': article, 
                                    'code': 200})
        except:
            return response('Error parsing request', 400)
        
    
        
    if request.method == 'PUT':
        try:
            body: dict = json.loads(request.body)
            if body.get('article_id') == '':
                return response("Article ID not defined, rewrite and send request again", 400)
        
            article: Article = Article.objects.filter(article_id=body.get('article_id'))
            article.headline=body.get('headline'),
            article.author=body.get('author'),
            article.category=body.get('category'),
            article.date_time_edited=datetime.now(),
            article.contents=body.get('contents')
            article.save()
            
            return response("Successfully updated article", 200)
        except:
            return response("Error parsing article update, check request again", 400)
    
    if request.method == 'DELETE':    
        try:
            body: dict = json.loads(request.body)
            article: Article = Article.objects.filter(article_id=body.get('article_id'))
            article.delete()
            return response('Article deleted successfully', 200)
        except:
            return response('Error parsing request', 400)
    

# Comment endpoints

## POST
def create_comment(request: HttpRequest) -> HttpResponse:
    try:
        body: dict = json.loads(request.body)
        new_comment = Comment(
            posted_by=body.get('posted_by'),
            date_time_posted=datetime.now(),
            date_time_edited=datetime.now(),
            contents=body.get('contents')
        )
        new_comment.save()
        return response('Comment created successfully', 200)
    except:
        return response('Error parsing new comment object, check request again', 400)

## GET
def get_comments() -> HttpResponse:
    all_comments = model_to_dict(Comment.objects.all())
    return HttpResponse({'comments': all_comments, 'code': 200})

def get_comment(request: HttpRequest) -> HttpResponse:
    try:
        body: dict = json.loads(request.body)
        article: Article = Article.objects.filter(article_id=body.get('article_id'))
        if (article is None): #If get returns empty object
            return response('Article not found', 404)
        else:
            return HttpResponse({'article': article, 
                                 'code': 200})
    except:
        return response('Error parsing request', 400)

## PUT
def update_comment(request: HttpRequest) -> HttpResponse:
    try:
        body: dict = json.loads(request.body)
        if body.get('article_id') == '':
            return response("Comment ID not defined, rewrite and send request again", 400)
        
        comment: Comment = Comment.objects.filter(comment_id=body.get('comment_id'))
        comment.date_time_edited=datetime.now(),
        comment.contents=body.get('contents')
        comment.save()
        
        return response("Successfully updated artcommenticle", 200)
    except:
        return response("Error parsing comment update, check request again", 400)

## DELETE
def delete_comment(request: HttpRequest) -> HttpResponse:
    try:
        body: dict = json.loads(request.body)
        comment: Comment = Comment.objects.filter(comment_id=body.get('comment_id'))
        comment.delete()
        return response('Comment deleted successfully', 200)
    except:
        return response('Error parsing request', 400)