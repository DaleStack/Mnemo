from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def home_page(request):
    user = request.user
    return render(request, 'folders/home.html', {'user':user})