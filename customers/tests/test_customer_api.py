"""Tests for customer creation API endpoints."""

from datetime import date, timedelta

import pytest
from rest_framework.test import APIClient

CREATE_CUSTOMER_URL = "/api/v1/create_customer/"


@pytest.fixture
def api_client() -> APIClient:
    """Return an API client instance."""
    return APIClient()


@pytest.mark.django_db
def test_create_customer_success(api_client: APIClient) -> None:
    """A valid payload should create a customer and return HTTP 201."""

    payload = {
        "first_name": "Ben",
        "last_name": "Stokes",
        "dob": "1991-06-25",
    }

    response = api_client.post(
        CREATE_CUSTOMER_URL,
        payload,
        format="json",
    )

    assert response.status_code == 201
    assert response.data["data"]["first_name"] == "Ben"


@pytest.mark.django_db
def test_create_customer_with_future_dob_returns_400(
    api_client: APIClient,
) -> None:
    """A future date of birth should be rejected with HTTP 400."""

    payload = {
        "first_name": "Ben",
        "last_name": "Stokes",
        "dob": str(date.today() + timedelta(days=2)),
    }

    response = api_client.post(
        CREATE_CUSTOMER_URL,
        payload,
        format="json",
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_create_customer_without_first_name_returns_400(
    api_client: APIClient,
) -> None:
    """Omitting first_name should return HTTP 400."""

    payload = {
        "last_name": "Stokes",
        "dob": "1991-06-25",
    }

    response = api_client.post(
        CREATE_CUSTOMER_URL,
        payload,
        format="json",
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_create_customer_without_dob_returns_400(
    api_client: APIClient,
) -> None:
    """Omitting date of birth should return HTTP 400."""

    payload = {
        "first_name": "Ben",
        "last_name": "Stokes",
    }

    response = api_client.post(
        CREATE_CUSTOMER_URL,
        payload,
        format="json",
    )

    assert response.status_code == 400