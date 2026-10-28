
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Review


@receiver(post_save, sender=Review)
@receiver(post_delete, sender=Review)
def invalidate_doctor_cache_on_review_change(sender, **kwargs):
    cache.clear()
