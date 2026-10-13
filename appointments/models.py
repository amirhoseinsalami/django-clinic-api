from django.db import models
from django.conf import settings
from doctors.models import DoctorProfile


class Appointment(models.Model):

    class Status(models.TextChoices):

        PENDING = 'PEDNING', 'Pending'
        CONFIRMED = 'CONFIRMED', 'Confirmed'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'


    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.PROTECT,
        related_name='appointments'
    )

    appointment_time = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    class Meta:

        ordering = [
            '-appointment_time'
        ]

        constraints = [
            models.UniqueConstraint(

                fields = [
                    'doctor',
                    'appointment_time'
                ],
                
                name = 'unique_doctor_time'
            )
        ]

    def __str__(self):
        return f'{self.patient} - {self.doctor}'