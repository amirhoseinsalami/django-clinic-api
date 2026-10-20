import pytest

from rest_framework.test import APIClient

from accounts.models import User

from doctors.models import DoctorProfile

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def patient():

    return User.objects.create_user(
        username='patient1',
        password='pass123456',
        role="PATIENT"
    )

@pytest.fixture
def doctor():

    user = User.objects.create_user(
        username='doctor1',
        password='passdoc123456',
        role="DOCTOR"
    )

    return DoctorProfile.objects.create(
        user=user,
        experienced_years=5,
        consultation_fee=500000
    )