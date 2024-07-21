import smtplib
from celery import shared_task
from django.core.mail import send_mail
from config import settings
from materials.models import Course


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
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=email_list,
            fail_silently=False,
        )
    except smtplib.SMTPException as e:
        server_response = e
    return server_response
