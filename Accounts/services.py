from django.contrib.auth import authenticate
from django.apps import apps

from rest_framework.response import Response
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Employee, Company


class AccountingService:
    def generate_opt(self):
        pass

    def login_otp(self):
        pass

    @staticmethod
    def login_password(data: dict, account_class: str) -> Response:
        user = authenticate(phone_number=data["phone_number"], password=data["password"])
        if user and user.is_active:
            account = apps.get_model("Accounts", account_class).objects.get(user=user)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response({
                'access_token': access_token,
                'refresh_token': refresh_token,
                'account_id': account.id
            })

        raise serializers.ValidationError("Incorrect credentials.")

    def logout(self):
        pass
