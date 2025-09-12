from django.shortcuts import render, redirect
from .models import UserModel
from .forms import UserCreationForm
from django.contrib.auth import login
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

    return render(request, 'users/login.html', {'form': form})
