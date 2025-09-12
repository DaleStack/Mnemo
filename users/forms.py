from django.contrib.auth.forms import UserCreationForm
from .models import UserModel

class UserCreationForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ['username', 'email']
