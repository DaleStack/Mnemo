from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import TaskModel, CommentModel, UserEmailNotification
from folders.models import FolderModel

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


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.folder = FolderModel.objects.create(
            user=self.user,
            subject_name='Mathematics'
        )
        self.task = TaskModel.objects.create(
            folder=self.folder,
            title='Read Chapter 1',
            description='Read and summarize chapter 1.',
            created_by=self.user
        )

    def test_create_comment(self):
        comment = CommentModel.objects.create(
            task=self.task,
            user=self.user,
            content='This is a test comment.'
        )

        # Ensure comment is created
        self.assertIsNotNone(comment.id)
        self.assertEqual(comment.task, self.task)
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.content, 'This is a test comment.')

    def test_str_method_returns_first_20_chars(self):
        content_text = "This is a very long comment that should be truncated."
        comment = CommentModel.objects.create(
            task=self.task,
            user=self.user,
            content=content_text
        )
        self.assertEqual(str(comment), content_text[:20])

class UserEmailNotificationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.folder = FolderModel.objects.create(
            user=self.user,
            subject_name='Mathematics'
        )
        self.task = TaskModel.objects.create(
            folder=self.folder,
            title='Read Chapter 1',
            created_by=self.user
        )

    def test_create_user_email_notification(self):
        notif = UserEmailNotification.objects.create(
            user=self.user,
            task=self.task,
            reminder_sent=True,
            deadline_sent=False
        )

        # Ensure notification is created
        self.assertIsNotNone(notif.id)
        self.assertEqual(notif.user, self.user)
        self.assertEqual(notif.task, self.task)
        self.assertTrue(notif.reminder_sent)
        self.assertFalse(notif.deadline_sent)
        self.assertIsNotNone(notif.reminder_sent_at)
        self.assertIsNotNone(notif.deadline_sent_at)

    def test_str_method(self):
        notif = UserEmailNotification.objects.create(
            user=self.user,
            task=self.task
        )
        expected_str = f"Notifications for {self.user.username} on task {self.task.title}"
        self.assertEqual(str(notif), expected_str)