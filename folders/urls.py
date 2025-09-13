from django.urls import path
from .views import home_page, create_folder, join_folder, folder_view, leave_folder, delete_folder

urlpatterns = [
    path('home/', home_page, name='home'),
    path('create-folder/', create_folder, name='create_folder'),
    path('join-folder/', join_folder, name='join_folder'),
    path('folder/<int:folder_id>/', folder_view, name='folder_view'),
    path('folders/<int:folder_id>/leave/', leave_folder, name='leave_folder'),
    path('folders/<int:folder_id>/delete/', delete_folder, name='delete_folder'),
]
