from django.db import models

from Accounts.models import Employee, Company
from .Enum import *
from Bases.base_models import BaseModel


class Gift(BaseModel):
    amount = models.PositiveIntegerField()
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, related_name='gift')
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, related_name='gift')


class Wallet(BaseModel):
    total_amount = models.PositiveIntegerField(default=0)
    gift_amount = models.PositiveIntegerField(default=0)
    credit_amount = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, related_name='wallet')


class WalletTransaction(BaseModel):
    type = models.IntegerField(choices=WalletTransactionEnums.Types.choices)
    source = models.IntegerField(choices=WalletTransactionEnums.Sources.choices)
    amount = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    wallet = models.ForeignKey(Wallet, on_delete=models.DO_NOTHING, related_name='transactions')


class Transaction(BaseModel):
    transfer_mode = models.IntegerField(choices=TransactionEnum.Types.choices)
    transfer_id = models.CharField(max_length=20, blank=True)
    destination = models.CharField(max_length=100)
    destination_first_name = models.CharField(max_length=100)
    destination_last_name = models.CharField(max_length=100)
    amount = models.PositiveBigIntegerField()
    commission = models.PositiveBigIntegerField()
    status = models.IntegerField(choices=TransactionEnum.Status.choices, default=TransactionEnum.Status.PENDING.value)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.set_unique_transfer_id()

        super(Transaction, self).save(*args, **kwargs)

    def set_unique_transfer_id(self):
        transfer_id = self.generate_transfer_id()
        while Transaction.objects.filter(transfer_id=transfer_id).exists():
            transfer_id = self.generate_transfer_id()

        self.transfer_id = transfer_id

    @staticmethod
    def generate_transfer_id():
        import random
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
        return str("".join(random.choice(chars) for _ in range(9)))
