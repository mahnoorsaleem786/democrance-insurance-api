import datetime
import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_create_customer_success():

    client = APIClient()

    payload = {
        "first_name": "Ben",
        "last_name": "Stokes",
        "dob": "1991-06-25",
    }

    response = client.post(
        "/api/v1/create_customer/",
        payload,
        format="json",
    )

    assert response.status_code == 201

    assert response.data["data"]["first_name"] == "Ben"

@pytest.mark.django_db
def test_future_dob():

    client = APIClient()

    payload = {
        "first_name": "Ben",
        "last_name": "Stokes",
        "dob": str(
            datetime.date.today() +
            datetime.timedelta(days=2)
        ),
    }

    response = client.post(
        "/api/v1/create_customer/",
        payload,
        format="json",
    )

    assert response.status_code == 400

@pytest.mark.django_db
def test_missing_first_name():

    client = APIClient()

    payload = {
        "last_name": "Stokes",
        "dob": "1991-06-25",
    }

    response = client.post(
        "/api/v1/create_customer/",
        payload,
        format="json",
    )

    assert response.status_code == 400

@pytest.mark.django_db
def test_missing_dob():

    client = APIClient()

    payload = {
        "first_name": "Ben",
        "last_name": "Stokes",
    }

    response = client.post(
        "/api/v1/create_customer/",
        payload,
        format="json",
    )

    assert response.status_code == 400