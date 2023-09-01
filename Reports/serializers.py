from rest_framework import serializers

from Treasury.models import WalletTransaction


class WalletTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = WalletTransaction
        fields = '__all__'
