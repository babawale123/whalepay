from django.urls import path
from .views import PurchaseVerificationAPIView,Purchases


urlpatterns = [
    path('',PurchaseVerificationAPIView.as_view()),
    path('payments/',Purchases.as_view())
]