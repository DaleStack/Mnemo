from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import FolderModel

User = get_user_model()

class FolderModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_folder_creation_generates_unique_code(self):
        folder = FolderModel.objects.create(
            user=self.user,
            subject_name='Mathematics'
        )

        # Ensure folder is created
        self.assertIsNotNone(folder.id)

        # Ensure code is generated and has length 8
        self.assertIsNotNone(folder.code)
        self.assertEqual(len(folder.code), 8)

        # Ensure code is uppercase alphanumeric
        self.assertTrue(folder.code.isalnum())
        self.assertTrue(folder.code.isupper())

    def test_folder_str_returns_subject_name(self):
        folder = FolderModel.objects.create(
            user=self.user,
            subject_name='Science'
        )
        self.assertEqual(str(folder), 'Science')
