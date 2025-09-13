from django.shortcuts import render, redirect, get_object_or_404
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

@login_required
def folder_view(request, folder_id):
    # Only get the folder if the current user is a member
    folder = get_object_or_404(FolderModel, id=folder_id, members__user=request.user)

    # Get the current user's membership (to know their role)
    membership = FolderMember.objects.get(folder=folder, user=request.user)

    return render(
        request,
        'folders/folder_detail.html',
        {
            'folder': folder,
            'membership': membership
        }
    )

    
@login_required
def leave_folder(request, folder_id):
    """Let a member leave the folder (but owner cannot leave)."""
    folder = get_object_or_404(FolderModel, id=folder_id, members__user=request.user)

    # Get the membership
    membership = get_object_or_404(FolderMember, folder=folder, user=request.user)

    # Prevent owner from leaving their own folder
    if membership.role == 'owner':
        messages.error(request, "Owners cannot leave their own folder. Delete it instead.")
        return redirect('folder_view', folder_id=folder.id)

    # Delete membership
    membership.delete()
    messages.success(request, f"You have left the folder: {folder.subject_name}")
    return redirect('home')


@login_required
def delete_folder(request, folder_id):
    """Let the owner delete the folder and all its members/tasks."""
    folder = get_object_or_404(FolderModel, id=folder_id, members__user=request.user)

    # Verify the user is owner
    membership = get_object_or_404(FolderMember, folder=folder, user=request.user)
    if membership.role != 'owner':
        messages.error(request, "Only the owner can delete this folder.")
        return redirect('folder_view', folder_id=folder.id)

    # Delete the folder (will cascade to members/tasks)
    folder.delete()
    messages.success(request, "Folder deleted successfully.")
    return redirect('home')
