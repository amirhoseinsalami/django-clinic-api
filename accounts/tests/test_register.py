import pytest

from rest_framework.test import APIClient

from accounts.models import User


@pytest.mark.django_db  #means this test needs database.
def test_user_can_register():

    client = APIClient()

    response = client.post(
        'api/acoounts/register/',
        {
            'username' : 'amir',
            'email' : 'amir@gmail.com',
            'password' : 'amir123456' 
        }
    )

    assert response.status_code == 201

    assert User.objects.filter(username='amir').exists()
