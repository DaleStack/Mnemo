from celery import shared_task
from django.core.mail import send_mail
from django.urls import reverse
from .models import TaskModel, UserEmailNotification
from django.utils import timezone

@shared_task
def send_task_created_email(task_id):
    """
    Send email notifications to all members of the folder
    whenever a new task is created.
    """
    task = TaskModel.objects.get(id=task_id)
    folder = task.folder
    members = folder.members.all()  # FolderMember objects

    base_url = "http://localhost:8000"
    task_url = base_url + reverse('task_detail', args=[folder.id, task.id])

    for member in members:
        send_mail(
            subject=f'New Task Created: {task.title}',
            message=(
                f"A new task has been created in folder '{folder.subject_name}'.\n\n"
                f"Title: {task.title}\n"
                f"Description: {task.description or 'No description'}\n"
                f"Due Date: {task.due_date or 'No due date'}\n\n"
                f"View Task: {task_url}"
            ),
            from_email='no-reply@mnemo.local',
            recipient_list=[member.user.email],
            fail_silently=True
        )

@shared_task
def check_and_send_reminders():
    today = timezone.now().date()
    # Get tasks whose reminder date is today or earlier
    tasks = TaskModel.objects.filter(reminder_date__lte=today)

    for task in tasks:
        for member in task.folder.members.all():
            notif, created = UserEmailNotification.objects.get_or_create(
                user=member.user,
                task=task
            )

            # Only send if reminder not sent yet
            if not notif.reminder_sent:
                task_url = f"http://localhost:8000" + reverse('task_detail', args=[task.folder.id, task.id])

                send_mail(
                    subject=f'Reminder: {task.title}',
                    message=(
                        f"This is a reminder for the task '{task.title}' in folder '{task.folder.subject_name}'.\n\n"
                        f"Description: {task.description or 'No description'}\n"
                        f"Due Date: {task.due_date or 'No due date'}\n\n"
                        f"View Task: {task_url}"
                    ),
                    from_email='no-reply@mnemo.local',
                    recipient_list=[member.user.email],
                    fail_silently=True
                )

                notif.reminder_sent = True
                notif.reminder_sent_at = timezone.now()
                notif.save()
