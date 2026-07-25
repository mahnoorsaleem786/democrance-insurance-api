from django.urls import path

from .views import CreateQuoteAPIView

urlpatterns = [
    path(
        "quote/",
        CreateQuoteAPIView.as_view(),
        name="create-quote",
    ),
]