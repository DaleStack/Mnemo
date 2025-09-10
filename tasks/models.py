from django.db import models
from folders.models import FolderModel
from django.conf import settings
from pgvector.django import VectorField
# Create your models here.

PRIORITY_CHOICES = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
]

class TaskModel(models.Model):
    folder = models.ForeignKey(FolderModel, 
                               on_delete=models.CASCADE, 
                               related_name='tasks')
    title = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    task_link = models.URLField(max_length=500, null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    reminder_date = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    embedding = models.VectorField(dimensions=768, null=True, blank=True)
    

