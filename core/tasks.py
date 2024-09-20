from celery import shared_task
from django.conf import settings
from notification.service import NotificationService


@shared_task
def create_flight_notifications():
    service = NotificationService(
        settings.TELEGRAM_BOT_TOKEN, settings.TELEGRAM_CHAT_ID
    )
    service.send_reminiscent_notification()
