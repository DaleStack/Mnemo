from django.urls import path
from .views import home_page, create_folder, join_folder

urlpatterns = [
    path('home/', home_page, name='home'),
    path('create-folder/', create_folder, name='create_folder'),
    path('join-folder/', join_folder, name='join_folder'),
]
