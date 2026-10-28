
import logging
import smtplib

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from .models import Appointment


logger = logging.getLogger(__name__)


@shared_task(
    autoretry_for=(OSError, smtplib.SMTPException),
    retry_backoff=10,
    retry_jitter=True,
    retry_kwargs={"max_retries": 3},
)
def send_appointment_email(appointment_id):
    try:
        appointment = (
            Appointment.objects
            .select_related("patient", "doctor__user")
            .get(pk=appointment_id)
        )
    except Appointment.DoesNotExist:
        logger.warning(
            "Appointment %s does not exist.",
            appointment_id,
        )
        return "appointment_not_found"

    recipient = appointment.patient.email

    if not recipient:
        logger.warning(
            "Patient for appointment %s has no email address.",
            appointment_id,
        )
        return "missing_recipient"

    doctor_user = appointment.doctor.user
    doctor_name = (
        doctor_user.get_full_name()
        or doctor_user.username
    )

    appointment_time = timezone.localtime(
        appointment.appointment_time
    ).strftime("%Y-%m-%d %H:%M %Z")

    subject = "Appointment request received"

    message = (
        f"Hello {appointment.patient.username},\n\n"
        "We have received your appointment request.\n\n"
        f"Appointment ID: {appointment.id}\n"
        f"Doctor: {doctor_name}\n"
        f"Date and time: {appointment_time}\n"
        f"Status: {appointment.get_status_display()}\n\n"
        "This email confirms receipt of your request. "
        "Please check the appointment status for confirmation.\n"
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient],
        fail_silently=False,
    )

    logger.info(
        "Appointment email sent for appointment %s.",
        appointment_id,
    )

    return "sent"


@shared_task
def send_appointment_reminders():
    tomorrow = timezone.localdate() + timezone.timedelta(days=1)

    appointments = (
        Appointment.objects
        .filter(appointment_time__date=tomorrow)
        .select_related("patient", "doctor__user")
    )

    for appointment in appointments:
        logger.info(
            "Reminder candidate: appointment %s",
            appointment.id,
        )
