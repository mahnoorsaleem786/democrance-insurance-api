"""Tests for customer search API endpoints."""

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from customers.models import Customer

TOKEN_URL = "/api/token/"
CUSTOMER_LIST_URL = "/api/v1/customers/"


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
def test_search_customer_by_name(
    authenticated_client: APIClient,
) -> None:
    """Authenticated requests should filter customers by name."""

    Customer.objects.create(
        first_name="Ben",
        last_name="Stokes",
        dob="1991-06-25",
    )

    response = authenticated_client.get(
        f"{CUSTOMER_LIST_URL}?name=Ben",
    )

    assert response.status_code == 200
    assert len(response.data) == 1