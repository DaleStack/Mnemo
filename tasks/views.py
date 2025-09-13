from django.shortcuts import render, redirect, get_object_or_404
from .models import TaskModel
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CreateTaskForm
from folders.models import FolderModel, FolderMember
from django.views.decorators.http import require_POST
# Create your views here.

@login_required
def create_task(request, folder_id):
    folder = get_object_or_404(FolderModel, id=folder_id, members__user=request.user)

    if request.method == 'POST':
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.folder = folder
            task.created_by = request.user
            task.save()
            messages.success(request, 'Task created successfully!')
        else:
            messages.error(request, 'Error creating task.')

    # Always go back to the folder view after form submit
    return redirect('folder_view', folder_id=folder.id)

@login_required
@require_POST
def delete_task(request, folder_id, task_id):
    """Delete a task if the user is a member of the folder."""
    folder = get_object_or_404(FolderModel, id=folder_id, members__user=request.user)
    task = get_object_or_404(folder.tasks, id=task_id)  # ensures the task belongs to the same folder

    # Optional: Only the creator or folder owner can delete
    membership = FolderMember.objects.get(folder=folder, user=request.user)
    if task.created_by != request.user and membership.role != 'owner':
        messages.error(request, "You don't have permission to delete this task.")
        return redirect('folder_view', folder_id=folder.id)

    task.delete()
    messages.success(request, 'Task deleted successfully.')
    return redirect('folder_view', folder_id=folder.id)

    