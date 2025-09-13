from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import FolderModel, FolderMember
from .forms import CreateFolderForm
from django.contrib import messages
# Create your views here.

@login_required
def home_page(request):
    user = request.user
    folders = FolderModel.objects.filter(user=user)
    return render(request, 'folders/home.html', {'user':user, 'folders': folders})

@login_required
def create_folder(request):
    if request.method == 'POST':
        form = CreateFolderForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.user = request.user
            folder.save()

            FolderMember.objects.create(
                folder=folder,
                user=request.user,
                role='owner'
            )

            messages.success(request, 'Folder created successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Error creating folder. Try again.')
            return redirect('home')
    else:
        return redirect('home')

    
    
                  