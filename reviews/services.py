from django.core.exceptions import ValidationError
from appointments.models import Appointment
from .models import Review

def create_review(appointment, patient, rating, comment):

    if appointment.patient != patient:
        raise ValidationError("This is not your appointment")

    if appointment.status != "COMPLETED":
        raise ValidationError('You can review only completed appointments')

    if hasattr(appointment, 'review'):
        raise ValidationError('Already reviewed')

    return Review.objects.create(
        appointment=appointment,
        patient=patient,
        doctor=appointment.doctor,
        rating=rating,
        comment=comment
    )