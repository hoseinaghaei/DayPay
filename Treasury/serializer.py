from rest_framework import serializers

from Bases.base_serializers import BaseSerializer

from .models import Wallet


class AddGiftSerializer(BaseSerializer):
    employee_id = serializers.IntegerField()
    amount = serializers.IntegerField()

    def validate_employee_id(self):
        pass

    def validate_amount(self):
        pass


class WithdrawCreditSerializer(BaseSerializer):
    amount = serializers.IntegerField()
    wallet_id = serializers.IntegerField()
    type = serializers.CharField(max_length=100)  # todo : ChoiceField

    def validate_amount(self):
        pass

    def validate_wallet_id(self):
        pass

    def validate_type(self):
        pass


class GetCreditSerializer(BaseSerializer):
    credit_amount = serializers.IntegerField()


class GetWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('total_amount', 'gift_amount', 'credit_amount')


class DepositCreditSerializer(BaseSerializer):
    credit_amount = serializers.IntegerField()
    wallet_id = serializers.IntegerField()

    def validate_credit_amount(self):
        pass

    def validate_wallet_id(self):
        pass
