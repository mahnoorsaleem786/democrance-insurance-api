"""Tests for quote creation API endpoints."""

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from customers.models import Customer

TOKEN_URL = "/api/token/"
QUOTE_URL = "/api/v1/quote/"


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
def test_create_quote_success(
    authenticated_client: APIClient,
) -> None:
    """A valid quote request should create a QUOTED policy."""

    customer = Customer.objects.create(
        first_name="Ben",
        last_name="Stokes",
        dob="1991-06-25",
    )

    response = authenticated_client.post(
        QUOTE_URL,
        {
            "customer_id": customer.id,
            "policy_type": "personal-accident",
        },
        format="json",
    )

    assert response.status_code == 201
    assert response.data["data"]["state"] == "QUOTED"


@pytest.mark.django_db
def test_create_quote_with_invalid_customer_returns_400(
    authenticated_client: APIClient,
) -> None:
    """Quote requests for unknown customers should return HTTP 400."""

    response = authenticated_client.post(
        QUOTE_URL,
        {
            "customer_id": 999,
            "policy_type": "personal-accident",
        },
        format="json",
    )

    assert response.status_code == 400