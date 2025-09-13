from celery import shared_task
from django.core.mail import send_mail
from django.urls import reverse
from .models import TaskModel, UserEmailNotification
from django.utils import timezone
from django.contrib.auth import get_user_model
from folders.models import FolderMember, FolderModel


BASE_URL = "http://localhost:8000"


def build_task_email_html(task, folder, task_url, heading, subtext):
    """Returns a minimal modern HTML email template."""
    # ... (this function remains the same)
    return f"""
    <div style="font-family: Arial, sans-serif; background-color: #f9fafb; padding: 40px;">
      <div style="max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 12px; padding: 30px; box-shadow: 0 2px 6px rgba(0,0,0,0.05);">
        <h2 style="color: #111827; font-size: 24px; margin-bottom: 10px;">{heading}</h2>
        <p style="color: #6b7280; font-size: 14px; margin-bottom: 25px;">{subtext}</p>
        
        <div style="border-top: 1px solid #e5e7eb; padding-top: 15px; margin-top: 15px;">
          <p style="color: #374151; font-size: 15px; margin: 5px 0;"><strong>Task:</strong> {task.title}</p>
          <p style="color: #374151; font-size: 15px; margin: 5px 0;"><strong>Description:</strong> {task.description or 'No description'}</p>
          <p style="color: #374151; font-size: 15px; margin: 5px 0;"><strong>Due Date:</strong> {task.due_date or 'No due date'}</p>
        </div>
        
        <a href="{task_url}" 
           style="display: inline-block; background: #3b82f6; color: #ffffff; text-decoration: none; 
                  padding: 12px 20px; margin-top: 30px; border-radius: 8px; font-size: 15px;">
           View Task
        </a>
      </div>
    </div>
    """


@shared_task
def send_task_created_email(task_id):
    # ... (this function remains the same)
    task = TaskModel.objects.get(id=task_id)
    folder = task.folder
    task_url = BASE_URL + reverse('task_detail', args=[folder.id, task.id])

    for member in folder.members.all():
        html_content = build_task_email_html(
            task, folder, task_url,
            heading="📝 New Task Created",
            subtext=f"A new task has been created in folder <b>{folder.subject_name}</b>."
        )

        send_mail(
            subject=f'New Task Created: {task.title}',
            message=f"A new task '{task.title}' has been created. View it here: {task_url}",
            from_email='no-reply@mnemo.local',
            recipient_list=[member.user.email],
            html_message=html_content,
            fail_silently=True
        )


@shared_task
def check_and_send_reminders_and_deadlines():
    # ... (this function remains the same)
    today = timezone.now().date()
    tasks = TaskModel.objects.all()

    for task in tasks:
        for member in task.folder.members.all():
            notif, _ = UserEmailNotification.objects.get_or_create(
                user=member.user,
                task=task
            )

            task_url = BASE_URL + reverse('task_detail', args=[task.folder.id, task.id])

            # 📌 Reminder
            if task.reminder_date and task.reminder_date <= today and not notif.reminder_sent:
                html_content = build_task_email_html(
                    task, task.folder, task_url,
                    heading="⏰ Task Reminder",
                    subtext=f"This is a reminder for your task in <b>{task.folder.subject_name}</b>."
                )

                send_mail(
                    subject=f'Reminder: {task.title}',
                    message=f"Reminder for task '{task.title}'. View it here: {task_url}",
                    from_email='no-reply@mnemo.local',
                    recipient_list=[member.user.email],
                    html_message=html_content,
                    fail_silently=True
                )
                notif.reminder_sent = True
                notif.reminder_sent_at = timezone.now()

            # 📌 Deadline
            if task.due_date and task.due_date <= today and not notif.deadline_sent:
                html_content = build_task_email_html(
                    task, task.folder, task_url,
                    heading="⚡ Task Deadline Reached",
                    subtext=f"The task is now due in <b>{task.folder.subject_name}</b>."
                )

                send_mail(
                    subject=f'Deadline Reached: {task.title}',
                    message=f"Deadline reached for task '{task.title}'. View it here: {task_url}",
                    from_email='no-reply@mnemo.local',
                    recipient_list=[member.user.email],
                    html_message=html_content,
                    fail_silently=True
                )
                notif.deadline_sent = True
                notif.deadline_sent_at = timezone.now()

            notif.save()


@shared_task
def send_notifications_for_new_folder_member(user_id, folder_id):
    """
    Sends a one-time notification for all existing tasks in the
    specific folder a user has just joined.
    """
    User = get_user_model()
    try:
        user = User.objects.get(id=user_id)
        # Use the specific folder_id passed to the task
        folder = FolderModel.objects.get(id=folder_id) 
    except (User.DoesNotExist, FolderModel.DoesNotExist):
        return # Exit if user or folder not found

    # Iterate only through the tasks in the newly joined folder
    for task in folder.tasks.all():
        notif, created = UserEmailNotification.objects.get_or_create(
            user=user,
            task=task
        )

        # Only send if the "joined" email has not been sent before.
        # This check is still valuable as a safeguard.
        if not notif.joined_sent:
            task_url = BASE_URL + reverse('task_detail', args=[folder.id, task.id])

            html_content = build_task_email_html(
                task, folder, task_url,
                heading="📌 Task Assigned",
                subtext=f"You have joined <b>{folder.subject_name}</b>. Here's one of its existing tasks."
            )

            send_mail(
                subject=f'Assigned Task: {task.title}',
                message=f"You have been assigned task '{task.title}'. View it here: {task_url}",
                from_email='no-reply@mnemo.local',
                recipient_list=[user.email],
                html_message=html_content,
                fail_silently=True
            )

            # Mark that the email has been sent and save
            notif.joined_sent = True
            notif.joined_sent_at = timezone.now()
            notif.save()
