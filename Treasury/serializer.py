from rest_framework import serializers

from Bases.base_serializers import BaseSerializer

from .Enum import TransactionEnum


class GiftSerializer(BaseSerializer):
    employee_id = serializers.IntegerField()
    amount = serializers.IntegerField()


class WalletSerializer(BaseSerializer):
    employee_id = serializers.IntegerField()
    type = serializers.ChoiceField(choices=TransactionEnum.Types.choices, required=False)
