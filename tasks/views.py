from django.shortcuts import render, redirect, get_object_or_404
from .models import TaskModel
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CreateTaskForm
from folders.models import FolderModel
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

    