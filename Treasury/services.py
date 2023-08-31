from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.db.models import F, Sum
from django.db.models.functions import Coalesce

from .models import Gift, Employee, Wallet, WalletTransaction, Company, Transaction
from .Enum import WalletTransactionEnums, TransactionEnum
from Utils.date_time_utils import *
from Utils.otp_utils import *
from Utils.sms_utils import *
from Utils.jibit_utils import send_trnasacttion_to_jibit


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

            wallet = Wallet.objects.select_for_update().get(employee=employee)

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
        validate_otp(employee.user, data["otp"])
        with transaction.atomic():
            wallet = Wallet.objects.select_for_update().get(employee=employee, active=True)
            balance = wallet.total_amount

            self.create_wallet_transaction(
                wallet,
                WalletTransactionEnums.Types.WITHDRAW.value,
                WalletTransactionEnums.Sources.EMPLOYEE.value,
                balance
            )

            wallet.total_amount = 0
            wallet.credit_amount = 0
            wallet.gift_amount = 0
            wallet.save(update_fields=["total_amount", "credit_amount", "gift_amount"])

            trx = Transaction.objects.get(transfer_id=data["transfer_id"])
            try:
                send_trnasacttion_to_jibit()
            except Exception as e:
                send_trnasacttion_to_jibit()

            trx.status = TransactionEnum.Status.SENT_TO_BANK.value
            trx.save(update_fields=["status"])

            return Response(
                data={
                    'amount': balance,
                    'transfer_id': trx.transfer_id,
                    'type': data['transfer_mode'],
                    'sheba_number': employee.sheba_number
                },
                status=status.HTTP_200_OK
            )

    @staticmethod
    def get_wallet(employee_id: int):
        wallet = Wallet.objects.get(employee_id=employee_id, active=True)

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

        max_credit = round((day_of_month / day_in_month) * (employee.credit_rate_limit / 100) * employee.salary)
        withdraw_credit_in_month = self.get_taken_credit_in_current_month(employee=employee)
        return max_credit - withdraw_credit_in_month

    @staticmethod
    def get_taken_credit_in_current_month(employee: Employee):
        first_day_of_month = jalali_first_day_of_month()
        return WalletTransaction.objects.filter(
            wallet=employee.wallet.get(active=True),
            type=WalletTransactionEnums.Types.DEPOSIT,
            source=WalletTransactionEnums.Sources.EMPLOYEE,
            date__gte=first_day_of_month
        ).aggregate(total_amount=Coalesce(Sum('amount'), 0)).get("total_amount")

    @staticmethod
    def get_company_remaining_credit(company_id: int):
        company = Company.objects.get(id=company_id)
        return company.max_credit_limit - company.given_credit

    @staticmethod
    def has_company_enough_credit(company_id: int, credit: int):
        return TreasuryService.get_company_remaining_credit(company_id) >= credit

    def get_withdraw_detail(self, data: dict):
        wallet = Wallet.objects.get(employee_id=data["employee_id"], active=True)
        employee = Employee.objects.get(id=data["employee_id"])
        commission = self.get_commission(data["transfer_mode"], employee.company, wallet.total_amount)

        output = {
            "amount": wallet.total_amount,
            "commission": commission,
            "sheba_number": wallet.employee.sheba_number
        }

        return Response(data=output, status=status.HTTP_200_OK)

    @staticmethod
    def get_commission(transaction_type, company: Company, amount) -> int:
        if transaction_type == TransactionEnum.Types.REGULAR.value:
            commission = amount * company.regular_commission_rate / 100
        elif transaction_type == TransactionEnum.Types.FAST.value:
            commission = amount * company.fast_commission_rate / 100
        else:
            raise Exception('Illegal transaction type')

        return round(commission)

    def generate_withdraw_otp(self, data: dict):
        employee = Employee.objects.get(id=data['employee_id'], is_active=True)
        wallet = employee.wallet.get(active=True)
        otp_code = generate_otp_and_set_on_cache(employee.user, 6000)

        trx = Transaction.objects.create(
            transfer_mode=data['transfer_mode'],
            destination=employee.sheba_number,
            destination_first_name=employee.first_name,
            destination_last_name=employee.last_name,
            amount=wallet.total_amount,
            commission=self.get_commission(data["transfer_mode"], employee.company, wallet.total_amount)
        )

        send_withdraw_otp(otp_code, employee.user.phone_number)

        return Response(
            {
                "transfer_id": trx.transfer_id,
                "otp": otp_code,
                "message": "success",
            },
            status=status.HTTP_200_OK
        )
