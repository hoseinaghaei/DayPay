from django.contrib.auth import authenticate
from django.apps import apps
from django.core.cache import cache

from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Employee, Company, Users
from .utils import otp_generator


class AccountingService:
    def generate_opt(self, data: dict) -> Response:
        user = Users.object.get(phone_number=data["phone_number"])
        if user and user.is_active:
            otp_code = self._generate_otp_and_set_on_cache(user.id)
            return Response(
                {
                    "otp": otp_code,
                },
                status=status.HTTP_200_OK
            )

        raise serializers.ValidationError("Incorrect credentials.")

    @staticmethod
    def _generate_otp_and_set_on_cache(user_id: int):
        otp_code = otp_generator()
        cache_key = f"user_otp:{user_id}"
        old_opt = cache.get(cache_key)
        if old_opt:
            cache.delete(cache_key)

        cache.set(cache_key, otp_code, timeout=120)
        return otp_code

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
