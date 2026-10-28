
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models.signals import (
    m2m_changed,
    post_delete,
    post_save,
)
from django.dispatch import receiver

from .models import DoctorAvailability, DoctorProfile, Speciality


# Changes to doctor-related data can make cached API responses stale.
@receiver(post_save, sender=DoctorProfile)
@receiver(post_delete, sender=DoctorProfile)
@receiver(post_save, sender=DoctorAvailability)
@receiver(post_delete, sender=DoctorAvailability)
@receiver(post_save, sender=Speciality)
@receiver(post_delete, sender=Speciality)
def invalidate_doctor_related_cache(sender, **kwargs):
    cache.clear()


# Changing a doctor's specialities doesn't save the DoctorProfile itself.
@receiver(m2m_changed, sender=DoctorProfile.specialities.through)
def invalidate_doctor_cache_on_speciality_change(
    sender,
    action,
    **kwargs,
):
    if action in {"post_add", "post_remove", "post_clear"}:
        cache.clear()


# Doctor usernames or names may also appear in the API response.
User = get_user_model()


@receiver(post_save, sender=User)
def invalidate_doctor_cache_on_user_change(sender, instance, **kwargs):
    try:
        instance.doctor_profile
    except DoctorProfile.DoesNotExist:
        return

    cache.clear()
