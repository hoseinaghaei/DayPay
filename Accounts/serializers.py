from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=12)
    username = serializers.CharField(max_length=150, required=False)
    password = serializers.CharField(max_length=128, required=False)
    otp = serializers.CharField(max_length=5, required=False)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
