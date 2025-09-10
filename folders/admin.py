from django.contrib import admin
from .models import FolderModel, FolderMember
# Register your models here.

admin.site.register(FolderModel)
admin.site.register(FolderMember)

