from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import FolderModel, FolderMember

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


class FolderMemberModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.other_user = User.objects.create_user(username='otheruser', password='password123')

        self.folder = FolderModel.objects.create(
            user=self.user,
            subject_name='Mathematics'
        )

    def test_create_folder_member(self):
        member = FolderMember.objects.create(
            folder=self.folder,
            user=self.other_user,
            role='member'
        )

        # Ensure member is created
        self.assertIsNotNone(member.id)
        self.assertEqual(member.folder, self.folder)
        self.assertEqual(member.user, self.other_user)
        self.assertEqual(member.role, 'member')

    def test_str_method(self):
        member = FolderMember.objects.create(
            folder=self.folder,
            user=self.other_user,
            role='admin'
        )
        expected_str = f"{self.other_user.username} - {self.folder.subject_name} (admin)"
        self.assertEqual(str(member), expected_str)

    def test_unique_together_constraint(self):
        # First membership is fine
        FolderMember.objects.create(folder=self.folder, user=self.other_user)

        # Second should raise IntegrityError
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            FolderMember.objects.create(folder=self.folder, user=self.other_user)
