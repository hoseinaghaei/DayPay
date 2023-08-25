from rest_framework import serializers

from Bases.base_serializers import BaseSerializer


class LoginSerializer(BaseSerializer):
    phone_number = serializers.CharField(max_length=12)
    username = serializers.CharField(max_length=150, required=False)
    password = serializers.CharField(max_length=128, required=False)
    otp = serializers.CharField(max_length=6, required=False)
