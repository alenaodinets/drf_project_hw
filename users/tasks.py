import pytz
from celery import shared_task
from config import settings
from datetime import datetime, timedelta
from users.models import User


@shared_task
def deactivate_users():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    users = User.objects.all().filter(is_active=True)
    for user in users:
        if current_datetime - user.last_login > timedelta(days=30):
            user.is_active = False
            user.save()