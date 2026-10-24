from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView 

from .models import Payment
from .services import create_payment
from .serializers import PaymentSerializer
from appointments.models import Appointment

from drf_spectacular.utils import extend_schema


class CreatePaymentView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    @extend_schema(request=PaymentSerializer, responses=PaymentSerializer)
    def post(self, request):
        appointment_id = request.data.get("appointment")

        try:
            appointment = Appointment.objects.get(id=appointment_id)

            payment = create_payment(
                appointment=appointment,
                user=request.user
            )

        except Appointment.DoesNotExist:
            return Response(
                {"detail": "Appointment not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = PaymentSerializer(payment)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class PaymentCallbackView(APIView):

    @extend_schema(exclude=True)
    def post(self, request):
        transaction_id = request.data.get('transcation_id')
        status_value = request.data.get('status')

        payment = Payment.objects.get(transcation_id=transaction_id)

        if status_value == 'SUCCESS':
            payment.status = Payment.Status.SUCCESS

            payment.save()

            return Response({'message' : 'Payment updated'})