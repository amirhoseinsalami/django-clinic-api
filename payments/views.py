from django.core.exceptions import ValidationError as DjangoValidationError
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from appointments.models import Appointment

from .models import Payment
from .serializers import PaymentSerializer
from .services import create_payment, complete_payment


class CreatePaymentView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=PaymentSerializer,
        responses=PaymentSerializer
    )
    def post(self, request):

        appointment_id = request.data.get("appointment")

        if not appointment_id:
            raise DRFValidationError({
                "appointment": "This field is required."
            })

        appointment = get_object_or_404(
            Appointment,
            id=appointment_id
        )

        try:
            payment = create_payment(
                appointment=appointment,
                user=request.user
            )

        except DjangoValidationError as e:
            raise DRFValidationError(e.messages)

        serializer = PaymentSerializer(payment)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class PaymentCallbackView(APIView):

    @extend_schema(exclude=True)
    def post(self, request):

        payment_id = request.data.get("payment")
        transaction_id = request.data.get("transaction_id")
        status_value = request.data.get("status")

        if not payment_id:
            return Response(
                {"detail": "payment is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not transaction_id:
            return Response(
                {"detail": "transaction_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        payment = get_object_or_404(
            Payment,
            id=payment_id
        )

        if status_value == "SUCCESS":

            complete_payment(
                payment=payment,
                transaction_id=transaction_id
            )

            payment.refresh_from_db()

            return Response({
                "message": "Payment completed successfully",
                "payment": PaymentSerializer(payment).data
            })

        if status_value == "FAILED":

            payment.status = Payment.Status.FAILED
            payment.save(update_fields=["status"])

            return Response({
                "message": "Payment failed"
            })

        return Response(
            {"detail": "Invalid payment status"},
            status=status.HTTP_400_BAD_REQUEST
        )