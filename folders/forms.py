from django import forms   
from .models import FolderModel

class CreateFolderForm(forms.ModelForm):
    class Meta:
        model = FolderModel
        fields = ['subject_name']