from django.http import HttpResponse, HttpRequest, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth.decorators import login_required
from time import sleep

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
