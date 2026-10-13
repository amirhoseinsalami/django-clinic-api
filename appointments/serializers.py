from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):

    patient = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Appointment

        fields = [
            'id',
            'patient',
            'doctor',
            'appointment_time',
            'status'
        ]

        read_only_fields = [
            'status'
        ]