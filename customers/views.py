"""API views for customer management."""

from django.db.models import Q
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Customer
from .serializers import CustomerSerializer


class CreateCustomerAPIView(CreateAPIView):
    """Create a new customer record."""

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """Validate input, persist the customer, and return a success payload."""

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        customer = serializer.save()

        return Response(
            {
                "message": "Customer created successfully.",
                "data": CustomerSerializer(customer).data,
            },
            status=status.HTTP_201_CREATED,
        )


class CustomerListAPIView(ListAPIView):
    """List customers with optional name and date-of-birth filters."""

    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter customers by optional query parameters."""

        queryset = Customer.objects.all()

        name = self.request.query_params.get("name")
        dob = self.request.query_params.get("dob")

        if name:
            queryset = queryset.filter(
                Q(first_name__icontains=name) |
                Q(last_name__icontains=name)
            )

        if dob:
            queryset = queryset.filter(dob=dob)

        return queryset
