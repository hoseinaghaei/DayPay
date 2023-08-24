from abc import ABC

from rest_framework import serializers
from .models import Wallet


class AddGiftSerializer(serializers.Serializer, ABC):
    employee_id = serializers.IntegerField()
    amount = serializers.IntegerField()

    def clean_employee_id(self):
        pass

    def clean_amount(self):
        pass


class WithdrawCreditSerializer(serializers.Serializer, ABC):
    amount = serializers.IntegerField()
    wallet_id = serializers.IntegerField()
    type = serializers.CharField(max_length=100)  # todo : ChoiceField

    def clean_amount(self):
        pass

    def clean_wallet_id(self):
        pass

    def clean_type(self):
        pass


class GetCreditSerializer(serializers.Serializer, ABC):
    credit_amount = serializers.IntegerField()


class GetWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('total_amount', 'gift_amount', 'credit_amount')


class DepositCreditSerializer(serializers.Serializer, ABC):
    credit_amount = serializers.IntegerField()
    wallet_id = serializers.IntegerField()

    def clean_credit_amount(self):
        pass

    def clean_wallet_id(self):
        pass
