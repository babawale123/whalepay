from decimal import Decimal

import requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

from payment.models import Purchase

from .serializer import PaymentVerificationSerializer, PurchaseSerializer








class Purchases(APIView):
    def get(self, request):
        purchases = Purchase.objects.filter(user=request.user)
        data = PurchaseSerializer(purchases, many=True).data
        return Response(data={'data': data})


class PurchaseVerificationAPIView(APIView):
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
            if(data['status'] == 'success'):
                transaction_data = data['data']
                tx_ref = transaction_data['tx_ref']
                tx_id = transaction_data['id']
                tx_amount = transaction_data['amount']
                if (float(amount) == float(tx_amount) and tx_ref == transaction_reference and tx_id == transaction_id):

                    return Response({"payment in progress"})
                   
                    new_purchase = Purchase.objects.create(
                        user=request.user,
                        reference=tx_ref,
                        note=f'You purchased {purchased_water_volume} litres of water',
                        amount=Decimal(amount)
                    )
                    request.user.water_balance += purchased_water_volume
                    request.user.save()
                    return Response({'data': {'message': f'Purchase Successful!. You have topped up your meter with {purchased_water_volume} litres of water'}})
                return Response("Invalid transaction")
            return Response("Sorry. There was an issue with your payment.")
        return Response(data.errors)
