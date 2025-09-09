from django.db import models
from django.conf import settings
import string
import random


# Create your models here.
class FolderModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=8, unique=True, blank=True)
    subject_name = models.CharField(max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def generate_unique_code(self):
        """Generate a unique 8-character alphanumeric code."""
        length = 8
        characters = string.ascii_uppercase + string.digits
        
        while True:
            code = ''.join(random.choice(characters) for _ in range(length))
            if not FolderModel.objects.filter(code=code).exists():
                return code

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_unique_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.subject_name
