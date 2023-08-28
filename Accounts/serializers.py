from rest_framework import serializers

from Bases.base_serializers import BaseSerializer
from Treasury.models import Wallet

from .models import Employee, Users


class LoginSerializer(BaseSerializer):
    phone_number = serializers.CharField(max_length=12)
    username = serializers.CharField(max_length=150, required=False)
    password = serializers.CharField(max_length=128, required=False)
    otp = serializers.CharField(max_length=6, required=False)


class EmployeeSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=12, required=False)

    class Meta:
        model = Employee
        exclude = ['is_active', 'user']

    def create(self, validated_data):
        phone_number = validated_data.pop('phone_number')
        user, created = Users.objects.get_or_create(phone_number=phone_number)
        employee = Employee.objects.create(user=user, **validated_data)
        wallet = Wallet.objects.create(employee=employee)
        return employee
