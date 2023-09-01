from rest_framework import serializers

from Bases.base_serializers import BaseSerializer

from .Enum import TransactionEnum


class GiftSerializer(BaseSerializer):
    employee_id = serializers.IntegerField()
    amount = serializers.IntegerField()


class WalletSerializer(BaseSerializer):
    employee_id = serializers.IntegerField()
    transfer_mode = serializers.ChoiceField(choices=TransactionEnum.Types.choices, required=False)
    otp = serializers.CharField(max_length=6, required=False)
    transfer_id = serializers.CharField(max_length=9, required=False)
