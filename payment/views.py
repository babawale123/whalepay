from decimal import Decimal
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Purchase  # Import your Purchase model
from .serializer import PurchaseSerializer, PaymentVerificationSerializer
from django.conf import settings
from rest_framework.decorators import authentication_classes,permission_classes
from rest_framework import permissions,authentication

class Purchases(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        # Make sure you import Purchase model and serializer correctly
        purchases = Purchase.objects.filter(user=request.user)
        data = PurchaseSerializer(purchases, many=True).data
        return Response(data)


class PurchaseVerificationAPIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        data = PaymentVerificationSerializer(data=request.data)
        if data.is_valid():
            validated_data = data.validated_data
            amount = validated_data.get("amount")
            transaction_reference = validated_data.get("transaction_reference")
            transaction_id = validated_data.get("transaction_id")
            verify_url = settings.FLUTTERWAVE_PAYMENT_VERIFICATION_URL.format(
                transaction_id)
            verify_response = requests.get(verify_url, headers={
                'Authorization': f'Bearer {settings.FLUTTERWAVE_SECRET_KEY}'
            })
            data = verify_response.json()
            if data.get('status') == 'success':  # Use get() to safely access dictionary keys
                transaction_data = data.get('data')
                tx_ref = transaction_data.get('tx_ref')
                tx_id = transaction_data.get('id')
                tx_amount = transaction_data.get('amount')
                if (
                    float(amount) == float(tx_amount) and
                    tx_ref == transaction_reference and
                    tx_id == transaction_id
                ):
                    # Create a new purchase object
                    new_purchase = Purchase.objects.create(
                        user=request.user,
                        reference=tx_ref,
                        note=f'You purchased litres of water',
                        amount=Decimal(amount)
                    )
                    # Return the serialized purchase data
                    serialized_purchase = PurchaseSerializer(new_purchase).data
                    return Response({"message": "Payment in progress", "purchase": serialized_purchase})
                return Response({"message": "Invalid transaction"})
            return Response({"message": "Sorry. There was an issue with your payment."})
        return Response(data.errors)
