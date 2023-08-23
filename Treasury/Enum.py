from django.db import models


class WalletTransactionEnums:

    class Types(models.IntegerChoices):
        DEPOSIT = 1, 'deposit'
        WITHDRAW = 2, 'withdraw'

    class Sources(models.IntegerChoices):
        EMPLOYEE = 1, 'employee'
        COMPANY = 2, 'company'

