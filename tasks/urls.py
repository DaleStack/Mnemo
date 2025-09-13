from django.urls import path

from .views import create_task, delete_task

urlpatterns = [
    path('folder/<int:folder_id>/create-task/', create_task, name='create_task'),
    path('folder/<int:folder_id>/tasks/<int:task_id>/delete/', delete_task, name='delete_task'),
]
