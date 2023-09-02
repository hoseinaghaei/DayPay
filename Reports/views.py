from Accounts.models import Company
from Bases.base_views import BaseAPIView
from .serializers import WalletTransactionSerializer
from .services import *
from Treasury.models import WalletTransaction


class CompanyTransactions(BaseAPIView):
    serializer_class = WalletTransactionSerializer

    def get(self, request):
        company_id = request.query_params.get("company_id")
        wallet_transactions = WalletTransaction.objects.filter(wallet__employee__company_id=company_id,
                                                               type=WalletTransactionEnums.Types.DEPOSIT)
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


class CompanyDetails(BaseAPIView):
    def get(self, request):
        company_id = request.query_params.get("company_id")
        try:
            return ReportsService().get_company_details(company_id)
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class EmployeeDetails(BaseAPIView):
    def get(self, request):
        employee_id = request.query_params.get("employee_id")
        try:
            return ReportsService().get_employee_details(employee_id)
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)