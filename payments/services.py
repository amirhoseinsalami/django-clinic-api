from django.db import transaction
from django.core.exceptions import ValidationError

from .models import Payment

@transaction.atomic
def create_payment(appointment, user):

    if hasattr(appointment, 'payment'):  # if not appointment.payment, then AttributeError
        raise ValidationError('Payment already exists')

    if appointment.patient != user:
        raise ValidationError('Not your payment')

    amount = appointment.doctor.consultation_fee

    payment = Payment.objects.create(
        appointment=appointment,
        amount=amount
    )

    return payment

@transaction.atomic
def complete_payment(payment, transaction_id):

    payment.status = Payment.Status.SUCCESS

    payment.transaction_id = transaction_id

    payment.save()


    appointment = payment.appointment

    appointment.status = appointment.Status.CONFIRMED

    appointment.save()    
