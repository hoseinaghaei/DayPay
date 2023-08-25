from django.db import models


class WalletTransactionEnums:
    class Statuses(models.IntegerChoices):
        PENDING = 1,
        DONE = 2,
        FAILED = 3

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
