from rest_framework.permissions import BasePermission

class IsPatientOrDoctor(BasePermission):

    def has_permission(self, request, view):    
        return (
            request.user.is_authenticated 
            and request.user.role in ['PATIENT', 'DOCTOR']
        )


class IsAppointmentOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.role == 'PATIENT':
            return obj.patient == user

        if user.role == "DOCTOR":
            return obj.doctor.user == user

        return False

