from django import forms
from .models import TaskModel

class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = TaskModel
        fields = ['title', 'description', 'task_link', 'due_date', 'reminder_date', 'priority']