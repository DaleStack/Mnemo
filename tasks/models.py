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
    embedding = VectorField(dimensions=768, null=True, blank=True)

    def save(self, *args, **kwargs):
        """if not self.embedding:
                # Use description if available, otherwise fallback to title
            text_to_embed = self.description or self.title
            self.embedding = get_embedding(text_to_embed)"""
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class CommentModel(models.Model):
    task = models.ForeignKey(TaskModel,
                             on_delete=models.CASCADE,
                             related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:20]
    
class UserEmailNotification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='user_notifications')
    task = models.ForeignKey(TaskModel, on_delete=models.CASCADE,
                             related_name='task_notifications')
    reminder_sent = models.BooleanField(default=False)
    deadline_sent = models.BooleanField(default=False)
    reminder_sent_at = models.DateTimeField(auto_now_add=True)
    deadline_sent_at = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return f"Notifications for {self.user.username} on task {self.task.title}"



