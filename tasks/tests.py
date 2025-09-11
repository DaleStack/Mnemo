from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import FolderModel, TaskModel

User = get_user_model()

class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.folder = FolderModel.objects.create(
            user=self.user,
            subject_name='Mathematics'
        )

    def test_create_task(self):
        task = TaskModel.objects.create(
            folder=self.folder,
            title='Read Chapter 1',
            description='Read and summarize chapter 1 of the math textbook.',
            priority='high',
            created_by=self.user
        )

        # Ensure task is created
        self.assertIsNotNone(task.id)
        self.assertEqual(task.folder, self.folder)
        self.assertEqual(task.created_by, self.user)
        self.assertEqual(task.priority, 'high')

    def test_str_method(self):
        task = TaskModel.objects.create(
            folder=self.folder,
            title='Finish Assignment',
            created_by=self.user
        )
        self.assertEqual(str(task), 'Finish Assignment')
