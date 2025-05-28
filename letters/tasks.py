from celery import shared_task
from django.utils import timezone
from .models import SummaryLetter
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)

@shared_task
def check_unread_letters():
    User = get_user_model()
    now = timezone.now()

    for user in User.objects.all():
        unread_count = SummaryLetter.objects.filter(user=user, sent=False).count()
        if unread_count > 0:
            logger.info(f"[{now}] User '{user.username}' has {unread_count} unread letter(s).")

    return "Checked unread letters for all users."
