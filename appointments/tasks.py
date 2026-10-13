from celery import shared_task

from django.utils import timezone

from datetime import timedelta

from .models import Appointment


@shared_task  #Celery can execute this function in the background.
def send_appointment_email(
    appointment_id
):

    print(
        f"Sending email for appointment {appointment_id}"
    )


@shared_task
def send_appointment_reminders():

    tomorrow = timezone.now() + timedelta(days=1)

    appointments = Appointment.objects.filter(
        appointment_time__date = tomorrow.date()
    )

    for appointment in appointments:
        print(f'Reminder sent to {appointment.patient.username}')