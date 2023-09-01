from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status

from Bases.base_views import BaseAPIView
from .serializers import WalletTransactionSerializer
from Treasury.models import WalletTransaction


class CompanyTransactions(BaseAPIView):
    serializer_class = WalletTransactionSerializer

    def get(self, request):
        company_id = request.query_params.get("company_id")
        wallet_transactions = WalletTransaction.objects.filter(wallet__employee__company_id=company_id)
        if wallet_transactions.exists():
            serializer = self.serializer_class(wallet_transactions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"error": str(WalletTransaction.DoesNotExist)}, status=status.HTTP_400_BAD_REQUEST)


class EmployeeTransactions(BaseAPIView):
    serializer_class = WalletTransactionSerializer

    def get(self, request):
        employee_id = request.query_params.get("employee_id")
        wallet_transactions = WalletTransaction.objects.filter(wallet__employee_id=employee_id)
        if wallet_transactions.exists():
            serializer = self.serializer_class(wallet_transactions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"error": str(WalletTransaction.DoesNotExist)}, status=status.HTTP_400_BAD_REQUEST)
