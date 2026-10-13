import pytest

from rest_framework.test import APIClient

from accounts.models import User

@pytest.mark.django_db
def test_user_can_login():

    user = User.objects.create_user(
        username='amir',
        password='amir123456'
    )

    client = APIClient()

    response = client.post(
        'api/login/',
        {
            'username' : 'amir',
            'password' : 'amir123456'
        }
    )

    assert response.status_code == 200

    assert 'access' in response.data

    assert 'refresh' in response.data