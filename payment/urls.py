from django.urls import path
from .views import PurchaseVerificationAPIView


urlpatterns = [
    path('',PurchaseVerificationAPIView.as_view())
]