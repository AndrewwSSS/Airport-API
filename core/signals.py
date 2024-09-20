from django.conf import settings
from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver

from core.models import Flight
from django.core.cache import cache

from notification.service import NotificationService


def invalidate_flights_cache() -> None:
    cache.delete_pattern("*.flights.*")


@receiver(pre_save, sender=Flight)
def capture_old_values(sender, instance, **kwargs):
    if instance.pk:
        old_instance = sender.objects.get(pk=instance.pk)
        instance.old_instance = old_instance


@receiver(post_save, sender=Flight)
def flight_post_save_signal(sender, instance, **kwargs):
    invalidate_flights_cache()

    if not instance.old_instance:
        return

    old_instance = instance.old_instance
    if instance.departure_time != old_instance.departure_time:
        service = NotificationService(
            settings.TELEGRAM_BOT_TOKEN,
            settings.TELEGRAM_CHAT_ID,
        )
        service.send_notification(
            settings.DEPARTURE_TIME_CHANGED_MESSAGE_PATTERN.format(
                route=instance.route,
                old_time=old_instance.departure_time,
                new_time=instance.departure_time,
            ),
        )


@receiver(post_delete, sender=Flight)
def flight_post_delete_signal(sender, **kwargs):
    invalidate_flights_cache()
