"""URL routes for policy-related API endpoints."""

from django.urls import path

from .views import (AcceptQuoteAPIView, CreateQuoteAPIView,
                    PolicyHistoryAPIView, PolicyListAPIView)

urlpatterns = [
    path(
        "quote/",
        CreateQuoteAPIView.as_view(),
        name="create-quote",
    ),

    path(
        "quote/accept/",
        AcceptQuoteAPIView.as_view(),
    ),

    path(
        "policies/<int:pk>/history/",
        PolicyHistoryAPIView.as_view(),
    ),

    path(
        "policies/",
        PolicyListAPIView.as_view(),
        name="policy-list",
    ),
]
