"""Tests for policy search API endpoints."""

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from customers.models import Customer
from policies.models import Policy

TOKEN_URL = "/api/token/"
POLICY_LIST_URL = "/api/v1/policies/"


@pytest.fixture
def api_client() -> APIClient:
    """Return an API client instance."""
    return APIClient()


@pytest.fixture
def authenticated_client(api_client: APIClient) -> APIClient:
    """Return an authenticated API client."""

    User.objects.create_user(
        username="admin",
        password="admin123",
    )

    token = api_client.post(
        TOKEN_URL,
        {
            "username": "admin",
            "password": "admin123",
        },
    ).data["access"]

    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {token}",
    )

    return api_client


@pytest.mark.django_db
def test_search_policy_by_type(
    authenticated_client: APIClient,
) -> None:
    """Authenticated requests should filter policies by type."""

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

    response = authenticated_client.get(
        f"{POLICY_LIST_URL}?type=personal-accident",
    )

    assert response.status_code == 200
    assert len(response.data) == 1