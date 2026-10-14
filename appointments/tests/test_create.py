import pytest

from rest_framework.test import APIClient

from accounts.models import User

from doctors.models import DoctorProfile

from django.utils import timezone
from datetime import timedelta


@pytest.mark.django_db
def test_patient_can_create_appointment():

    patient = User.objects.create_user(
        username='amir',
        password='reza1234',
        role="PATIENT"
    )

    doctor_user = User.objects.create_user(
        username='dr ali',
        password='ali121342',
        role='DOCTOR'
    )

    doctor = DoctorProfile.objects.create(
        user=doctor_user,
        experienced_years=10,
        consultation_fee=500000
    )

    client=APIClient()

    client.force_authenticate(
        user=patient  #Pretend this request comes from this user.
    )

    response = client.post(
        '/api/appointments/',
        {
            'doctor' : doctor.id,
            'appointment_time': timezone.now() + timedelta(days=5)
        }
    )

    assert response.status_code == 201



