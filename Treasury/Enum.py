from django.db import models


class WalletTransactionEnums:

    class Types(models.IntegerChoices):
        DEPOSIT = 1, 'deposit'
        WITHDRAW = 2, 'withdraw'

    class Sources(models.IntegerChoices):
        EMPLOYEE = 1, 'employee'
        COMPANY = 2, 'company'


class TransactionEnum:
    class Types(models.IntegerChoices):
        FAST = 1, 'fast'
        REGULAR = 2, 'regular'

    class Status(models.IntegerChoices):
        PENDING = 1, 'pending'
        SENT_TO_BANK = 2, 'sent_to_bank'
        PAID = 3, 'paid'
        CANCELLED = 4, 'cancelled'
