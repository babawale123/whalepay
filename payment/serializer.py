from rest_framework import serializers
from payment.models import Purchase


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['timestamp', 'note', 'id']


class PaymentVerificationSerializer(serializers.Serializer):
    transaction_reference = serializers.CharField()
    amount = serializers.FloatField()
    transaction_id = serializers.IntegerField()
