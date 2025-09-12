from django.shortcuts import render, redirect
from .models import UserModel
from .forms import UserCreationForm, UserLoginForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
# Create your views here.


def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful')
            return redirect('home')
        else:
            messages.error(request, 'Unsuccessful Registration')
    else:
        form = UserCreationForm()

    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Welcome back!')
                return redirect('home') 
            else:
                messages.error(request, 'Unsuccessful Authentication')
    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})
