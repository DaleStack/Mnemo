from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import FolderModel, FolderMember
from .forms import CreateFolderForm
from django.contrib import messages
# Create your views here.

@login_required
def home_page(request):
    user = request.user
    folders = FolderModel.objects.filter(members__user=user).distinct()
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

@login_required
def join_folder(request):
    if request.method == 'POST':
        code = request.POST.get('code')  # get the code from a form input
        try:
            folder = FolderModel.objects.get(code=code)
        except FolderModel.DoesNotExist:
            messages.error(request, 'Invalid folder code')
            return redirect('home')

        # prevent joining twice
        if FolderMember.objects.filter(folder=folder, user=request.user).exists():
            messages.info(request, 'You are already a member of this folder')
            return redirect('home')

        FolderMember.objects.create(
            folder=folder,
            user=request.user,
            role='member'
        )
        messages.success(request, f'Joined folder: {folder.subject_name}')
        return redirect('home')

    else:
        return redirect('home')
    
                  