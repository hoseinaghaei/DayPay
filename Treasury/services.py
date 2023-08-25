from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from .models import Gift, Employee, Wallet, WalletTransaction, Company, Transaction
from .Enum import WalletTransactionEnums
from .utils import *


class TreasuryService:
    @staticmethod
    def add_gift(data: dict) -> Response:
        with transaction.atomic():
            employee = Employee.objects.get(id=data['employee_id'])
            company = Company.objects.select_for_update().get(id=employee.company_id)
            if not TreasuryService.has_company_enough_credit(company_id=company.id, credit=data['amount']):
                return Response(
                    data={
                        'error': 'Company has not enough credit left!'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            Gift.objects.create(
                amount=data['amount'],
                employee=employee,
                company=employee.company
            )

            wallet = Wallet.objects.select_for_update().get(id=employee.wallet_id)
            WalletTransaction.objects.create(
                type=WalletTransactionEnums.Types.DEPOSIT,
                source=WalletTransactionEnums.Sources.COMPANY,
                amount=data['amount'],
                wallet=wallet
            )

            wallet.total_amount += data['amount']
            wallet.gift_amount += data['amount']
            wallet.save(force_update=True)

            company.given_credit += data['amount']
            company.save(force_update=True)

            return Response(status=status.HTTP_200_OK)

    @staticmethod
    def deposit_wallet(employee_id: int):
        employee = Employee.objects.get(id=employee_id)
        remaining_credit = TreasuryService.get_remaining_credit(employee_id)
        with transaction.atomic():
            company = Company.objects.select_for_update().get(id=employee.company_id)
            if not TreasuryService.has_company_enough_credit(company_id=company.id, credit=remaining_credit):
                return Response(
                    data={
                        'error': 'Company has not enough credit left!'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            wallet = Wallet.objects.select_for_update().get(id=employee.wallet_id)
            WalletTransaction.objects.create(
                type=WalletTransactionEnums.Types.DEPOSIT,
                source=WalletTransactionEnums.Sources.EMPLOYEE,
                amount=remaining_credit,
                wallet=wallet
            )

            wallet.total_amount += remaining_credit
            wallet.credit_amount += remaining_credit
            wallet.save(force_update=True)

            company.given_credit += remaining_credit
            company.save(force_update=True)

            return Response(status=status.HTTP_200_OK)

    @staticmethod
    def withdraw_wallet(data: dict):
        employee = Employee.objects.get(id=data['employee_id'])
        with transaction.atomic():
            wallet = Wallet.objects.select_for_update().get(id=employee.wallet_id)
            balance = employee.wallet.total_amount

            wallet_transaction = WalletTransaction.objects.create(
                type=WalletTransactionEnums.Types.WITHDRAW,
                source=WalletTransactionEnums.Sources.EMPLOYEE,
                status=WalletTransactionEnums.Statuses.PENDING,
                amount=balance,
                wallet=wallet
            )
            Transaction.objects.create(
                wallet_transaction=wallet_transaction,
                type=data['type']
            )

            wallet.objects.update(total_amount=0, credit_amount=0, gift_amount=0)
            return Response(
                data={
                    'tracking_code': wallet_transaction.id,
                    'status': WalletTransactionEnums.Statuses.PENDING,
                    'amount': balance,
                    'type': data['type']
                },
                status=status.HTTP_200_OK
            )

    @staticmethod
    def get_wallet(employee_id: int):
        wallet: Wallet = Employee.objects.get(id=employee_id).wallet
        return Response(
            data={
                'total_credit': wallet.total_amount,
                'credit_amount': wallet.credit_amount,
                'gift_amount': wallet.gift_amount
            },
            status=status.HTTP_200_OK
        )

    @staticmethod
    def get_remaining_credit(employee_id: int) -> int:
        employee = Employee.objects.get(id=employee_id)
        day_in_month = jalali_day_in_month()
        day_of_month = jalali_day_of_month()

        max_credit = (day_of_month / day_in_month) * (employee.credit_rate_limit / 100) * employee.salary
        withdraw_credit_in_month = TreasuryService.get_taken_credit_in_current_month(employee=employee)
        return max_credit - withdraw_credit_in_month

    @staticmethod
    def get_taken_credit_in_current_month(employee: Employee):
        first_day_of_month = jalali_first_day_of_month()
        return WalletTransaction.objects.filter(
            wallet=employee.wallet,
            type=WalletTransactionEnums.Types.DEPOSIT,
            source=WalletTransactionEnums.Sources.EMPLOYEE,
            date__gte=first_day_of_month
        ).aggregate(sum('amount')).get('amount__sum', 0)

    @staticmethod
    def get_company_remaining_credit(company_id: int):
        company = Company.objects.get(id=company_id)
        return company.max_credit_limit - company.given_credit

    @staticmethod
    def has_company_enough_credit(company_id: int, credit: int):
        return TreasuryService.get_company_remaining_credit(company_id) >= credit
