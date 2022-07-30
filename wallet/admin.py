from django.contrib import admin

from wallet.models import *


# Custom Admin - Wallet
class WalletAdmin(admin.ModelAdmin):
    pass


# Custom Admin -Transaction
class TransactionAdmin(admin.ModelAdmin):
    pass


# Custom Admin - Redeemed Transaction
class RedeemedTransactionAdmin(admin.ModelAdmin):
    pass


# Model Registrations
admin.site.register(Wallet, WalletAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(RedeemedTransaction, RedeemedTransactionAdmin)