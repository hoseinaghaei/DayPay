from django.contrib import admin

from .models import *


@admin.register(Gift)
class GiftAdmin(admin.ModelAdmin):
    pass


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    pass


@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):
    pass
