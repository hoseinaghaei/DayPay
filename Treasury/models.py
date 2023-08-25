from django.db import models

from Accounts.models import Employee, Company
from .Enum import *
from Bases.base_models import BaseModel


class Gift(BaseModel):
    amount = models.PositiveIntegerField()
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, related_name='gift')
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, related_name='gift')


class Wallet(BaseModel):
    total_amount = models.PositiveIntegerField()
    gift_amount = models.PositiveIntegerField()
    credit_amount = models.PositiveIntegerField()
    active = models.BooleanField(default=True)

    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, related_name='wallet')


class WalletTransaction(BaseModel):
    type = models.IntegerField(choices=WalletTransactionEnums.Types.choices)
    source = models.IntegerField(choices=WalletTransactionEnums.Sources.choices)
    status = models.IntegerField(choices=WalletTransactionEnums.Statuses.choices,
                                 default=WalletTransactionEnums.Statuses.DONE)
    amount = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    wallet = models.ForeignKey(Wallet, on_delete=models.DO_NOTHING, related_name='transactions')


class Transaction(BaseModel):
    wallet_transaction = models.ForeignKey(WalletTransaction, on_delete=models.DO_NOTHING)
    type = models.IntegerField(choices=TransactionEnum.Type.choices)
    tracking_code = models.CharField(max_length=20, blank=True)
    is_processed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
