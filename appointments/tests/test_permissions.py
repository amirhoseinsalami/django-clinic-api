import pytest

from rest_framework.test import APIClient

from accounts.models import User

from appointments.models import Appointment

from doctors.models import DoctorProfile

@pytest.mark.django_db
def test_patient_cannot_see_other_patient_appointment():

    patient1 = User.objects.create_user(
        username='amir',
        password='reza1234',
        role="PATIENT"
       )

    patient2 = User.objects.create_user(
        username='ali',
        password='ali6251',
        role="PATIENT"
       )

    doctor_user = User.objects.create_user(
    username="dr ali",
    password="ali6251",
    role="DOCTOR"
)

    doctor = DoctorProfile.objects.create(
        user=doctor_user
    )

    appointment = Appointment.objects.create(
        patient=patient2,
        doctor=doctor,
        appointment_time="2026-10-20T10:00:00"
    )

    client = APIClient()

    client.force_authenticate(
        patient=patient1
    )

    response = client.get(
        f'/api/appointments/{appointment.id}/'
    )

    assert response.status_code == 404  # Because from the user's perspective:This object does not exist;This prevents information leakage.


@pytest.mark.django_db
def test_cannot_book_same_time_twice():

    patient1 = User.objects.create_user(
        username='amir',
        password='reza1234',
        role="PATIENT"
       )

    patient2 = User.objects.create_user(
        username='amir2',
        password='amir2pass',
        role="PATIENT"
       )

    doctor = User.objects.create_user(
        username='dr ali',
        password='ali6251',
        role="DOCTOR"
       )

    

    client = APIClient()

    client.force_authenticate(
        user=patient1
    )

    first = client.post(
        f'/api/appointments/',
        {
            'doctor' : doctor.id,
            'appointment_time' : '2024-10-9T10:30:00'
        }
    )

    client.force_authenticate(
        user=patient2
    )

    second = client.post(
        f'/api/appointments/',
        {
            'doctor' : doctor.id,
            'appointment_time' : '2024-10-9T10:30:00'
        }
    )


    assert first.status_code == 201

    assert second.status_code == 400