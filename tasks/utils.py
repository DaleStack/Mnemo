from django.core.mail import send_mail
from folders.models import FolderMember
from django.conf import settings

def send_task_created_email(task, task_url):
    """Send email notification to all members when a new task is created."""
    
    # Get all emails of members in the same folder
    member_emails = FolderMember.objects.filter(
        folder=task.folder
    ).values_list('user__email', flat=True)

    subject = f"[Mnemo] New Task: {task.title}"

    # Plain text fallback
    message = (
        f"A new task has been created in folder: {task.folder.subject_name}\n\n"
        f"Title: {task.title}\n"
        f"Description: {task.description or 'No description'}\n"
        f"Priority: {task.priority.capitalize()}\n"
        f"Due date: {task.due_date or 'No due date'}\n\n"
        f"View the task here: {task_url}"
    )

    # HTML version (clickable link)
    html_message = f"""
        <p>A new task has been created in <strong>{task.folder.subject_name}</strong></p>
        <ul>
            <li><strong>Title:</strong> {task.title}</li>
            <li><strong>Description:</strong> {task.description or 'No description'}</li>
            <li><strong>Priority:</strong> {task.priority.capitalize()}</li>
            <li><strong>Due date:</strong> {task.due_date or 'No due date'}</li>
        </ul>
        <p><a href="{task_url}" target="_blank">🔗 View Task</a></p>
    """

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        list(member_emails),
        fail_silently=True,
        html_message=html_message
    )
