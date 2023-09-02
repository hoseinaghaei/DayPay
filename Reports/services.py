from django.db.models import Count, Sum
from django.db.models.functions import Coalesce
from rest_framework.response import Response
from rest_framework import status


from Accounts.Enums import EmployeeEnums
from Accounts.models import Employee, Company
from Treasury.models import WalletTransaction, WalletTransactionEnums, TransactionEnum, Transaction
from Utils.date_time_utils import *


class ReportsService:

    def get_company_details(self, company_id: int) -> Response:
        company = Company.objects.get(id=company_id)
        data = {
            'name': company.name,
            'credits_details': {
                'current_month': self.get_monthly_transactions(company_id, jalali_get_month()),
                'previous_month': self.get_monthly_transactions(company_id, jalali_get_month() - 1),
                'last_6_months': self.get_last_6_months_transactions(company_id)
            },
            'employees_details': self.get_employees_count(company_id),
        }

        return Response(data, status=status.HTTP_200_OK)

    def get_last_6_months_transactions(self, company_id: int):
        data = {}
        month = jalali_get_month()
        for i in range(6):
            data[month - i] = self.get_monthly_transactions(company_id, month - i)
        return data

    @staticmethod
    def get_monthly_transactions(company_id: int, month: int):
        return WalletTransaction.objects.filter(
            wallet__employee__company_id=company_id,
            type=WalletTransactionEnums.Types.DEPOSIT,
            date__month=month
        ).aggregate(total_amount=Coalesce(Sum('amount'), 0), count=Count('id'))

    @staticmethod
    def get_employees_count(company_id: int) -> dict:
        employee_counts = (
            Employee.objects.filter(company_id=company_id).values('status').annotate(status_count=Count('status')))

        status_counts = {}
        for item in employee_counts:
            status_counts[EmployeeEnums.Status(item['status']).label] = item['status_count']

        return status_counts

    def get_employee_details(self, employee_id) -> Response:
        employee = Employee.objects.get(id=employee_id)
        data = {
            'first_name': employee.first_name,
            'last_name': employee.last_name,
            'company': employee.company.name,
            'transactions': self.get_transaction_details(employee_id)
        }

        return Response(data=data, status=status.HTTP_200_OK)

    @staticmethod
    def get_transaction_details(employee_id: int):
        first_day_of_month = jalali_first_day_of_month()
        trxs = WalletTransaction.objects.filter(
            wallet__employee_id=employee_id,
            type=WalletTransactionEnums.Types.WITHDRAW.value,
            date__gte=first_day_of_month
        ).values('transfer_id__transfer_mode'
                 ).annotate(count=Count('transfer_id__transfer_mode'))

        data = {
            'total_count': 0,
            TransactionEnum.Types.FAST.label: 0,
            TransactionEnum.Types.REGULAR.label: 0
        }

        for transaction in trxs:
            data['total_count'] += transaction['count']
            data[TransactionEnum.Types(transaction['transfer_id__transfer_mode']).label] += transaction['count']

        return data
