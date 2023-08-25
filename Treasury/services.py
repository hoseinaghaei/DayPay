from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.db.models import F

from .models import Gift, Employee, Wallet, WalletTransaction, Company, Transaction
from .Enum import WalletTransactionEnums
from .utils import *


class TreasuryService:

    def add_gift(self, data: dict) -> Response:
        with transaction.atomic():
            employee = Employee.objects.get(id=data['employee_id'])
            company = Company.objects.select_for_update().get(id=employee.company_id)
            if not self.has_company_enough_credit(company_id=company.id, credit=data['amount']):
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

            wallet = Wallet.objects.select_for_update().get(employee=employee)

            self.create_wallet_transaction(
                wallet,
                WalletTransactionEnums.Types.DEPOSIT.value,
                WalletTransactionEnums.Sources.COMPANY.value,
                data['amount']
            )

            self.update_wallet_balance(wallet, gift_amount=data['amount'])

            self.update_company_balance(company, data['amount'])

            return Response(status=status.HTTP_200_OK)

    def deposit_wallet(self, employee_id: int):
        employee = Employee.objects.get(id=employee_id)
        remaining_credit = self.get_remaining_credit(employee_id)
        with transaction.atomic():
            company = Company.objects.select_for_update().get(id=employee.company_id)
            if not self.has_company_enough_credit(company_id=company.id, credit=remaining_credit):
                return Response(
                    data={
                        'error': 'Company has not enough credit left!'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            wallet = Wallet.objects.select_for_update().get(id=employee.wallet_id)

            self.create_wallet_transaction(
                wallet,
                WalletTransactionEnums.Types.DEPOSIT.value,
                WalletTransactionEnums.Sources.EMPLOYEE,
                remaining_credit
            )

            self.update_wallet_balance(wallet, credit_amount=remaining_credit)

            self.update_company_balance(company, remaining_credit)

            return Response(status=status.HTTP_200_OK)

    @staticmethod
    def update_company_balance(company, amount):
        company.given_credit = F("given_credit") + amount
        company.save(force_update=True)

    @staticmethod
    def create_wallet_transaction(wallet: Wallet, transaction_type, source, amount):
        wallet_trx = WalletTransaction.objects.create(
            type=transaction_type,
            source=source,
            amount=amount,
            wallet=wallet
        )

        return wallet_trx

    @staticmethod
    def update_wallet_balance(wallet: Wallet, credit_amount: int = 0, gift_amount: int = 0):
        wallet.gift_amount = F('gift_amount') + gift_amount
        wallet.credit_amount = F('credit_amount') + credit_amount
        wallet.total_amount = F('total_amount') + gift_amount + credit_amount
        wallet.save(force_update=True)

    def withdraw_wallet(self, data: dict):
        employee = Employee.objects.get(id=data['employee_id'])
        with transaction.atomic():
            wallet = Wallet.objects.select_for_update().get(employee=employee, active=True)
            balance = wallet.total_amount

            wallet_transaction = self.create_wallet_transaction(
                wallet,
                WalletTransactionEnums.Types.WITHDRAW.value,
                WalletTransactionEnums.Sources.EMPLOYEE.value,
                balance
            )

            Transaction.objects.create(
                wallet_transaction=wallet_transaction,
                type=data['type']
            )

            wallet_transaction.status = WalletTransactionEnums.Statuses.PENDING.value
            wallet_transaction.save(update_fields=["status"])

            wallet.objects.update(total_amount=0, credit_amount=0, gift_amount=0)
            return Response(
                data={
                    'tracking_code': wallet_transaction.id,
                    'status': WalletTransactionEnums.Statuses.PENDING.name,
                    'amount': balance,
                    'type': data['type']
                },
                status=status.HTTP_200_OK
            )

    @staticmethod
    def get_wallet(employee_id: int):
        wallet = Wallet.objects.get(employee_id=employee_id, active=True)

        if not wallet.exists():
            raise Exception("Wallet not Found")

        return Response(
            data={
                'total_credit': wallet.total_amount,
                'credit_amount': wallet.credit_amount,
                'gift_amount': wallet.gift_amount
            },
            status=status.HTTP_200_OK
        )

    def get_remaining_credit(self, employee_id: int) -> int:
        employee = Employee.objects.get(id=employee_id)
        day_in_month = jalali_day_in_month()
        day_of_month = jalali_day_of_month()

        max_credit = (day_of_month / day_in_month) * (employee.credit_rate_limit / 100) * employee.salary
        withdraw_credit_in_month = self.get_taken_credit_in_current_month(employee=employee)
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