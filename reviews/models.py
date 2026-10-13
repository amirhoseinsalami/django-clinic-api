from django.db import models
from django.conf import settings
from appointments.models import Appointment
from doctors.models import DoctorProfile


class Review(models.Model):

    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.PROTECT,
        related_name='review'
    )

    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    rating = models.PositiveSmallIntegerField()

    comment = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
        )

    class Meta:
        ordering = [
            '-created_at'
        ]

    def __str__(self):
        return f'{self.patient} reviewes {self.doctor}'