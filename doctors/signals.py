from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Speciality


SPECIALITIES_CACHE_KEY = "clinic:specialities:v1"


@receiver(post_save, sender=Speciality)
@receiver(post_delete, sender=Speciality)
def invalidate_specialities_cache(sender, **kwargs):
    cache.delete(SPECIALITIES_CACHE_KEY)
