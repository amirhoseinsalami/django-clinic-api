from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView 

from .models import Payment
from .services import create_payment
from .serializers import PaymentSerializer
from appointments.models import Appointment


class CreatePaymentView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):
        appointment_id = request.data.get('appointment')
        appointment = Appointment.objects.get(id=appointment_id)
        amount = request.data.get('amount')

        payment = create_payment(appointment_id, amount)

        serailizer = PaymentSerializer(payment)

        return Response(
            serailizer.data,
            status=status.HTTP_201_CREATED
        )


class PaymentCallbackView(APIView):

    def post(self, request):
        transaction_id = request.data.get('transcation_id')
        status_value = request.data.get('status')

        payment = Payment.objects.get(transcation_id=transaction_id)

        if status_value == 'SUCCESS':
            payment.status = Payment.Status.SUCCESS

            payment.save()

            return Response({'message' : 'Payment updated'})