from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Appointment
from .serializers import AppointmentSerializer
from .services import create_appointment, cancel_appointment
from .permissions import IsAppointmentOwner, IsPatientOrDoctor

from django.core.exceptions import ValidationError


class AppointmentViewSet(ModelViewSet):

    serializer_class = AppointmentSerializer

    permission_classes = [
        IsAuthenticated,
        IsPatientOrDoctor
    ]

    def get_queryset(self):
        user = self.request.user

        if user == 'PATIENT':
            return Appointment.objects.filter(patient=user).select_related('doctor', 'doctor__user')

        if user == 'DOCTOR':
            return Appointment.objects.filter(doctor__user=user).select_related('patient', 'doctor')

        return Appointment.objects.none()

    
    def get_permissions(self):

        if self.action in[
            'retrieve',
            'update',
            'partial_update',
            'destroy'
        ]:
            return (
                IsAuthenticated(),
                IsAppointmentOwner()
            )

        return super().get_permissions()  # check permissions in the permission_classes

    def perform_create(self, serializer):  # run on serializer.save() 
        
        user = self.request.user

        appointment = create_appointment(  # instead of Appointment.objects.create
            patient=user,
            doctor=serializer.validated_data['doctor'],
            appointment_time=serializer.validated_data['appointment_time']
        )


        serializer.instance = appointment   # Now the serailizer know whom should serilize 


    @action(detail=True, methods=['post']) # detail=True means Need object ID
    def cancel(self, request, pk=None):

        appointment = self.get_object()

        appointment = cancel_appointment(appointment, request.user)

        serializer = self.get_serializer(appointment)

        return Response(serializer.data)