from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = (
        ("PATIENT", "Patient"),
        ("DOCTOR", "Doctor"),
        ("ADMIN", "Admin"),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )


class PatientProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    phone = models.CharField(
        max_length=20
    )

    birth_date = models.DateField()

class DoctorProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    speciality = models.CharField(
        max_length=200
    )

    experience_years = models.IntegerField()


class Appointment(models.Model):

    patient = models.ForeignKey(
        PatientProfile,
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.PROTECT,
        related_name='appointments'
    )

    appointment_time = models.DateField()

    class Meta:
        Constraints = [
            models.UniqueConstraint(  # even in cuncurrent request, we sill not have similar appointment
                fields = [
                    'doctor',
                    'appointment_time'
                ],

                name = 'unique_doctor_time'
            )
        ]

    STATUS_CHOICES = [
        ("PENDING", 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )


class Payment(models.Model):

    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.PROTECT,
        related_name='payment'
    )

    amount = models.DecimalField(
        max_digit=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ("PENDING", "Pending"),
            ("PAID", 'Paid'),
            ("FAILED", 'Failed') 
        ]
    )

    transaction_id = models.CharField(
        max_length=100,
        null=True
    )
