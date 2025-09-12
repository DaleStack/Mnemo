from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import UserModel

class UserCreationForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ['username', 'email']


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
