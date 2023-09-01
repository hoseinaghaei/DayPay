from django.contrib import admin

from .models import *


@admin.register(Gift)
class GiftAdmin(admin.ModelAdmin):
    list_display = ['get_company', 'get_employee', 'amount']

    @admin.display(description='Employee')
    def get_employee(self, obj: Gift):
        return obj.employee

    @admin.display(description='Company')
    def get_company(self, obj: Gift):
        return obj.company


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['get_employee', 'total_amount', 'credit_amount', 'gift_amount', 'active']

    @admin.display(description='Employee')
    def get_employee(self, obj: Wallet):
        return obj.employee


@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = ['get_employee', 'type', 'source', 'amount', 'date']

    @admin.display(description='Employee')
    def get_employee(self, obj: WalletTransaction):
        return obj.wallet.employee


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Transaction._meta.get_fields()]
