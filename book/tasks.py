from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import BorrowRecord
from django.core.mail import send_mail

@shared_task
def send_due_date_notifications():
    seven_days_later = timezone.now().date() + timedelta(days=7)
    due_records = BorrowRecord.objects.filter(due_date__lte=seven_days_later, returned=False)

    for record in due_records:
        subject = 'Book Due Date Reminder'
        message = f'Dear {record.user.username}, your borrowed book "{record.book.title}" is due on {record.due_date}. Please return it soon.'
        send_mail(subject, message, 'library@example.com', [record.user.email])