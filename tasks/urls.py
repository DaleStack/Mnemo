from django.urls import path

from .views import create_task

urlpatterns = [
    path('folders/<int:folder_id>/create-task/', create_task, name='create_task'),
]
