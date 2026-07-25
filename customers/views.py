from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Customer
from .serializers import CustomerSerializer


class CreateCustomerAPIView(CreateAPIView):

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):

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