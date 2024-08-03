import smtplib
from celery import shared_task
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from materials.models import Course
import pytz
from celery import shared_task
from config import settings
from datetime import datetime, timedelta
from users.models import User

@shared_task
def send_email(pk, user):
    course = Course.objects.get(pk=pk)
    subs = course.subscription_set.all().filter(user=user)
    email_list = [user.email for subs.user in subs]
    message_subject = f"Обновление курса {course}"
    message_text = f"Обновление курса {course}"
    try:
        server_response = send_mail(
            subject=message_subject,
            message=message_text,
            from_email=EMAIL_HOST_USER,
            recipient_list=email_list,
            fail_silently=False,
        )
    except smtplib.SMTPException as e:
        server_response = e
    return server_response


@shared_task
def deactivate_users():
    current_datetime = datetime.now()
    users = User.objects.all().filter(is_active=True)
    for user in users:
        if current_datetime - user.last_login > timedelta(days=30):
            user.is_active = False
            user.save()