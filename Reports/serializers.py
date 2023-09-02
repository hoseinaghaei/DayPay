from rest_framework import serializers

from Treasury.models import WalletTransaction, Transaction, Wallet
from Accounts.serializers import EmployeeSerializer


class WalletSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()

    class Meta:
        model = Wallet
        fields = ['employee']


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ['transfer_mode', 'transfer_id', 'commission', 'status']


class WalletTransactionSerializer(serializers.ModelSerializer):
    transfer_id = TransactionSerializer(many=False, read_only=True)
    wallet = WalletSerializer()

    class Meta:
        model = WalletTransaction
        fields = '__all__'
