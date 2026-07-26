"""Tests for policy search API endpoints."""

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from customers.models import Customer
from policies.models import Policy


@pytest.mark.django_db
def test_search_policy_by_type():
    """Authenticated requests should filter policies by type."""

    User.objects.create_user(
        username="admin",
        password="admin123",
    )

    customer = Customer.objects.create(
        first_name="Ben",
        last_name="Stokes",
        dob="1991-06-25",
    )

    Policy.objects.create(
        customer=customer,
        policy_type="personal-accident",
        premium=200,
        cover=200000,
        state="ACTIVE",
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
        "/api/v1/policies/?type=personal-accident"
    )

    assert response.status_code == 200
    assert len(response.data) == 1
