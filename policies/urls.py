"""URL routes for policy-related API endpoints."""

from django.urls import URLPattern, path

from .views import (
    AcceptQuoteAPIView,
    CreateQuoteAPIView,
    PolicyHistoryAPIView,
    PolicyListAPIView,
)

urlpatterns: list[URLPattern] = [
    path(
        "quote/",
        CreateQuoteAPIView.as_view(),
        name="create-quote",
    ),
    path(
        "quote/accept/",
        AcceptQuoteAPIView.as_view(),
        name="accept-quote",
    ),
    path(
        "policies/<int:pk>/history/",
        PolicyHistoryAPIView.as_view(),
        name="policy-history",
    ),
    path(
        "policies/",
        PolicyListAPIView.as_view(),
        name="policy-list",
    ),
]