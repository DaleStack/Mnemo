from django.urls import path

from .views import create_task, delete_task, task_detail

urlpatterns = [
    path('folder/<int:folder_id>/create-task/', create_task, name='create_task'),
    path('folder/<int:folder_id>/tasks/<int:task_id>/delete/', delete_task, name='delete_task'),
    path('folders/<int:folder_id>/tasks/<int:task_id>/', task_detail, name='task_detail'),
]
