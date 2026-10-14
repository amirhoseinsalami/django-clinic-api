from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Appointment

from appointments.tasks import send_appointment_email


@transaction.atomic
def create_appointment(patient, doctor, appointment_time):

    if appointment_time < timezone.now():
        raise ValidationError('Can not book past time')

    if not doctor_is_available(doctor, appointment_time):
        raise ValidationError('Doctor is not avaiable at this time')


    exists = Appointment.objects.filter(
        doctor=doctor,
        appointment_time=appointment_time
    ).exists()

    if exists:
        raise ValidationError('This time is already booked')

    
    appointment = Appointment.objects.create(
        patient=patient,
        doctor=doctor,
        appointment_time=appointment_time
    )

    send_appointment_email.delay(
        appointment.id
    )

    return appointment


def doctor_is_available(doctor, appointment_time):

    exists = Appointment.objects.filter(
        doctor=doctor,
        appointment_time=appointment_time
    ).exists()

    return not exists


def cancel_appointment(appointment, user):

    if appointment.status == Appointment.Status.COMPLETED:
        raise ValidationError('Completed appointment can not be cancelled')

    if appointment.appointment_time < timezone.now():
        raise ValidationError('Past appointment can not be cancelled')

    if user.role == 'PATEINT':
        if appointment.patient != user:
            raise ValidationError('Not your appointent')

    elif user.role == 'DOCTOR':
        if appointment.doctor.user != user:
            raise ValidationError('Not your appointment')

    else:
        raise ValidationError('Permission denied!')

    appointment.status = Appointment.Status.CANCELLED

    appointment.save()

    return appointment


def confirm_appointment(appointment, user):

    if appointment.doctor.user != user:
        raise ValidationError('Only doctors can confirm')

    if appointment.status != Appointment.Status.PENDING:
        raise ValidationError('Invalid status')

    appointment.status = Appointment.Status.CONFIRMED

    appointment.save()

    return appointment