from django.urls import path
from .views import user_register, user_login, logout

urlpatterns = [
    path('register/', user_register, name='user_register'),
    path('login/', user_login, name='user_login'),
    path('logout/', logout, name='logout'),
]
