from rest_framework import serializers

from Bases.base_serializers import BaseSerializer
from Treasury.models import Wallet

from .models import Employee, Users


class LoginSerializer(BaseSerializer):
    phone_number = serializers.CharField(max_length=12)
    username = serializers.CharField(max_length=150, required=False)
    password = serializers.CharField(max_length=128, required=False)
    otp = serializers.CharField(max_length=6, required=False)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ['phone_number', 'email']


class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Employee
        exclude = ['is_active']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user, created = Users.objects.get_or_create(phone_number=user_data.get('phone_number'))
        employee = Employee.objects.create(user=user, **validated_data)
        Wallet.objects.create(employee=employee)
        return employee
