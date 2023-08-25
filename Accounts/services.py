from django.contrib.auth import authenticate
from django.apps import apps
from django.core.cache import cache

from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Employee, Company, Users
from .utils import *


class AccountingService:
    def generate_opt(self, data: dict) -> Response:
        user = Users.objects.get(phone_number=data["phone_number"])
        if user and user.is_active:
            otp_code = self._generate_otp_and_set_on_cache(user)
            return Response(
                {
                    "otp": otp_code,
                },
                status=status.HTTP_200_OK
            )

        raise serializers.ValidationError("Incorrect credentials.")

    @staticmethod
    def _generate_otp_and_set_on_cache(user: Users):
        otp_code, now = otp_generator(user.secret_key)
        old_opt = cache.get(get_otp_cache_key(user.id))
        if old_opt:
            cache.delete(get_otp_cache_key(user.id))

        cache.set(get_otp_cache_key(user.id), [otp_code, now], timeout=120)
        return otp_code

    def login_otp(self, data: dict, account_class: str) -> Response:
        user = Users.objects.get(phone_number=data["phone_number"])
        if user and user.is_active:
            stored_otp_data = cache.get(get_otp_cache_key(user.id))

            if not stored_otp_data:
                raise serializers.ValidationError("OTP expired or not generated.")

            if not validate_otp(user.secret_key, data["otp"], stored_otp_data[1]):
                raise serializers.ValidationError("OTP expired or not generated.")

            cache.delete(get_otp_cache_key(user.id))
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
