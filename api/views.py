import json
from django.http import HttpResponse, HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth.decorators import login_required
from .models import Article
from datetime import datetime

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

def create_article(request: HttpRequest) -> HttpResponse:
    try:
        body: dict = json.loads(request.body)
        new_article = Article(
            headline=body.get('headline'),
            author=body.get('author'),
            category=body.get('category'),
            date_time_posted=body.get('date_time_posted'),
            date_time_edited=body.get('date_time_edited'),
            contents=body.get('contents')
        )
        new_article.save()
        return HttpResponse({'message': 'Article created successfully',
                             'code': 200})
    except:
        return HttpResponse({'message': 'Error parsing new article object, check request again',
                             'code': 400})

def get_articles(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/article.html', {})

def update_article(request: HttpRequest) -> HttpResponse:
    try:
        body: dict = json.loads(request.body)
        if body.get('article_id') == '':
            return HttpResponse({'message': "Error finding article id, check request again",
                             'code': 400})
        
        article: Article = Article.objects.filter(article_id=body.get('article_id'))
        article.headline=body.get('headline'),
        article.author=body.get('author'),
        article.category=body.get('category'),
        article.date_time_posted=body.get('date_time_posted'),
        article.date_time_edited=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        article.contents=body.get('contents')
        article.save()
        
        return HttpResponse({'message': "Successfully updated article",
                            'code': 200})
    except:
        return HttpResponse({'message': "Error parsing article update, check request again",
                             'code': 400})
