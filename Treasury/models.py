from django.db import models

from Accounts.models import Employee, Company
from .Enum import *


class Gift(models.Model):
    amount = models.PositiveIntegerField()
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, related_name='gift')
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, related_name='gift')


class Wallet(models.Model):
    total_amount = models.PositiveIntegerField()
    gift_amount = models.PositiveIntegerField()
    credit_amount = models.PositiveIntegerField()

    active = models.BooleanField(default=True)
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, related_name='wallet')


class WalletTransaction(models.Model):
    type = models.IntegerField(choices=WalletTransactionEnums.Types.choices)
    source = models.IntegerField(choices=WalletTransactionEnums.Sources.choices)
    amount = models.PositiveIntegerField()

    data = models.DateTimeField(auto_now=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.DO_NOTHING, related_name='transactions')


class Transaction(models.Model):
    # wallet = models.ForeignKey(Wallet, on_delete=models.DO_NOTHING, related_name='transactions')
    pass
