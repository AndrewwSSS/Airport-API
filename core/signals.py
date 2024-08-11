from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Flight
from django.core.cache import cache


def invalidate_flights_cache() -> None:
    cache.delete_pattern("*.flights.*")


@receiver(post_save, sender=Flight)
def flight_post_save_signal(sender, **kwargs):
    invalidate_flights_cache()


@receiver(post_delete, sender=Flight)
def flight_post_delete_signal(sender, **kwargs):
    invalidate_flights_cache()
