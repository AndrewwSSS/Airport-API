from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Flight
from django.core.cache import cache


def invalidate_flights_cache() -> None:
    cache.delete_pattern("*.flights.*")


@receiver(post_save, sender=Flight)
def cache_save_invalidate(sender, **kwargs):
    invalidate_flights_cache()
    print("invalidate post save cache")


@receiver(post_delete, sender=Flight)
def cache_delete_invalidate(sender, **kwargs):
    invalidate_flights_cache()
    print("invalidate post delete cache")
