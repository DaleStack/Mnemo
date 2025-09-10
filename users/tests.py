# tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class UserModelTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='securepassword123'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('securepassword123'))
        self.assertIsNone(self.user.profile_pic.name)  # Should be default or blank

    def test_string_representation(self):
        self.assertEqual(str(self.user), 'testuser')
