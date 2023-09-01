from rest_framework.response import Response
from rest_framework import status

from Bases.base_views import BaseAPIView

from .serializer import GiftSerializer, WalletSerializer
from .services import TreasuryService


class GiftAPI(BaseAPIView):
    serializer_class = GiftSerializer

    def post(self, request):
        try:
            validated_data = self._prepare_validated_data(request)
            response = TreasuryService().add_gift(validated_data)
            return response
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DepositWalletApi(BaseAPIView):
    serializer_class = WalletSerializer

    def post(self, request):
        try:
            validated_data = self._prepare_validated_data(request)
            response = TreasuryService().deposit_wallet(employee_id=validated_data['employee_id'])
            return response
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetWithdrawDetails(BaseAPIView):
    serializer_class = WalletSerializer

    def post(self, request):
        try:
            validated_data = self._prepare_validated_data(request)
            response = TreasuryService().get_withdraw_detail(validated_data)
            return response
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GenerateWithdrawOTP(BaseAPIView):
    serializer_class = WalletSerializer

    def post(self, request):
        try:
            validated_data = self._prepare_validated_data(request)
            response = TreasuryService().generate_withdraw_otp(validated_data)
            return response
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class WithdrawWalletAPI(BaseAPIView):
    serializer_class = WalletSerializer

    def post(self, request):
        try:
            validated_data = self._prepare_validated_data(request)
            response = TreasuryService().withdraw_wallet(validated_data)
            return response
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetWalletApi(BaseAPIView):
    serializer_class = WalletSerializer

    def get(self, request):
        try:
            validated_data = self._prepare_validated_data(request)
            response = TreasuryService.get_wallet(employee_id=validated_data['employee_id'])
            return response
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetCreditApi(BaseAPIView):
    serializer_class = WalletSerializer

    def get(self, request):
        try:
            validated_data = self._prepare_validated_data(request)
            credit = TreasuryService().get_remaining_credit(employee_id=validated_data['employee_id'])
            return Response(data={'credit': credit}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
