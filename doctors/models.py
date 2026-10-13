from django.db import models

from django.conf import settings

class Speciality(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.name


class DoctorProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='doctor_profile'
    )

    speciality = models.ManyToManyField(
        Speciality,
        related_name='doctors'
    )

    bio = models.TextField(
        blank=True
    )

    experience_years = models.PositiveIntegerField(
        default=0
    )

    consultation_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    is_verified = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.user.username


class DoctorAvailability(models.Model):

    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.CASCADE,
        related_name = 'availability'
    )

    day_of_week = models.IntegerField(
        choices = [
            (0, 'Monday'),
            (1, 'Sunday'),
            (2, 'Tuesday'),
            (3, 'Wednesday'),
            (4, 'Thursday'),
            (5, 'Friday'),
            (6, 'Saturday')
        ]
    )

    start_time = models.TimeField()

    end_time = models.TimeField()


    def __str__(self):
        return (
            f'{self.doctor} - '
            f'{self.day_of_week}'
        )

        