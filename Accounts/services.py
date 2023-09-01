from django.contrib.auth import authenticate
from django.apps import apps
from django.core.cache import cache

from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Users
from Utils.otp_utils import *
from Utils.sms_utils import *


class AuthenticationService:
    def generate_opt(self, data: dict) -> Response:
        user = Users.objects.get(phone_number=data["phone_number"])
        if user and user.is_active:
            otp_code = generate_otp_and_set_on_cache(user)
            send_login_otp(otp_code, user.phone_number)
            return Response(
                {
                    "message": "success",
                },
                status=status.HTTP_200_OK
            )

        raise serializers.ValidationError("Incorrect credentials.")

    def login_otp(self, data: dict, account_class: str) -> Response:
        user = Users.objects.get(phone_number=data["phone_number"])
        if user and user.is_active:
            validate_otp(user, data["otp"])
            return self._create_auth_token(account_class, user)

        raise serializers.ValidationError("Incorrect credentials.")

    def login_password(self, data: dict, account_class: str) -> Response:
        user = authenticate(phone_number=data["phone_number"], password=data["password"])
        if user and user.is_active:
            return self._create_auth_token(account_class, user)

        raise serializers.ValidationError("Incorrect credentials.")

    @staticmethod
    def _create_auth_token(account_class: str, user: Users):
        account = apps.get_model("Accounts", account_class).objects.get(user=user, is_active=True)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return Response({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'account_id': account.id
        })

    def logout(self):
        pass
