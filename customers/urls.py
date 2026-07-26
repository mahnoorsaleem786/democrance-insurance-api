"""URL routes for customer-related API endpoints."""

from django.urls import URLPattern, path

from .views import CreateCustomerAPIView, CustomerListAPIView

urlpatterns: list[URLPattern] = [
    path(
        "create_customer/",
        CreateCustomerAPIView.as_view(),
        name="create-customer",
    ),
    path(
        "customers/",
        CustomerListAPIView.as_view(),
        name="customer-list",
    ),
]