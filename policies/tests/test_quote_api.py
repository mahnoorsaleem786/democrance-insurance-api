"""Tests for quote creation API endpoints."""

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from customers.models import Customer


@pytest.mark.django_db
def test_create_quote_success():
    """A valid quote request should create a QUOTED policy."""

    User.objects.create_user(
        username="admin",
        password="admin1234",
    )

    customer = Customer.objects.create(
        first_name="Ben",
        last_name="Stokes",
        dob="1991-06-25",
    )

    client = APIClient()

    token = client.post(
        "/api/token/",
        {
            "username": "admin",
            "password": "admin1234",
        },
    ).data["access"]

    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {token}"
    )

    response = client.post(
        "/api/v1/quote/",
        {
            "customer_id": customer.id,
            "policy_type": "personal-accident",
        },
        format="json",
    )

    assert response.status_code == 201
    assert response.data["data"]["state"] == "QUOTED"


@pytest.mark.django_db
def test_invalid_customer():
    """Quote requests for unknown customers should return HTTP 400."""

    User.objects.create_user(
        username="admin",
        password="admin123",
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

    response = client.post(
        "/api/v1/quote/",
        {
            "customer_id": 999,
            "policy_type": "personal-accident",
        },
        format="json",
    )

    assert response.status_code == 400
