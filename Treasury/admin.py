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
    pass


@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):
    pass
