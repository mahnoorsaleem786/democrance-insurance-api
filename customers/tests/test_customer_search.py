import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from customers.models import Customer


@pytest.mark.django_db
def test_search_customer_by_name():

    User.objects.create_user(
        username="admin",
        password="admin123",
    )

    Customer.objects.create(
        first_name="Ben",
        last_name="Stokes",
        dob="1991-06-25",
    )

    client = APIClient()

    token = client.post(
        "/api/token/",
        {
            "username": "admin",
            "password": "admin123",
        },
    ).data["access"]

    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {token}"
    )

    response = client.get(
        "/api/v1/customers/?name=Ben"
    )

    assert response.status_code == 200
    assert len(response.data) == 1