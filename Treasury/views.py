from rest_framework.response import Response
from rest_framework import status

from .serializer import AddGiftSerializer
from Bases.base_views import BaseAPIView
from .services import TreasuryService


class GiftAPI(BaseAPIView):
    serializer_class = AddGiftSerializer

    def post(self, request):
        try:
            validated_data = self._prepare_validated_data(request)
            response = TreasuryService.add_gift(validated_data)
            return response
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CreditAPI(BaseAPIView):
    serializer_class = None  # todo

    def post(self, request):
        try:
            validated_data = self._prepare_validated_data(request)
            response = TreasuryService.deposit_wallet(employee_id=validated_data['employee_id'])
            return response
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            validated_data = self._prepare_validated_data(request)
            credit = TreasuryService.get_remaining_credit(employee_id=validated_data['employee_id'])
            return Response(data={'credit': credit}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class WalletAPI(BaseAPIView):
    permission_classes = None  # todo

    def post(self, request):
        try:
            validated_data = self._prepare_validated_data(request)
            response = TreasuryService.withdraw_wallet(validated_data)
            return response
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            validated_data = self._prepare_validated_data(request)
            response = TreasuryService.get_wallet(employee_id=validated_data['employee_id'])
            return response
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
