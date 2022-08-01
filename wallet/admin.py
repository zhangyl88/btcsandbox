from django.contrib import admin

from wallet.models import *


# Custom Admin - Wallet
class WalletAdmin(admin.ModelAdmin):
    list_display            = ('user', 'r_balance', 'balance', 'profit', 'level',)
    readonly_fields         = ('id', 'user',)
    search_fields           = ('user__email', 'user__username', 'user__ip_address', 'user__id', 'level',)
    list_filter             = ('level',)
    
    fieldsets               = (
        (None, {'fields': ('r_balance', 'balance', 'profit', 'level',)}),
        ('Read-Only', {'fields': ('id', 'user',)}),
        ('Referrals', {'fields': ('referrals',)}),
    )


# Custom Admin -Transaction
class TransactionAdmin(admin.ModelAdmin):
    list_display            = ('user', 'reference', 'amount', 'transaction_type', 'timestamp',)
    readonly_fields         = ('id', 'user', 'reference', 'amount', 'transaction_type', 'timestamp',)
    search_fields           = ('user__email', 'user__username', 'user__ip_address', 'user__id', 'reference', 'transaction_type')
    list_filter             = ('transaction_type', 'status', 'timestamp', 'mode',)
    
    fieldsets               = (
        (None, {'fields': ('description', 'status',)}),
        ('Read-Only', {'fields': ('id', 'user', 'reference', 'amount', 'transaction_type', 'mode', 'timestamp',)}),
    )
    

# Custom Admin - Redeemed Transaction
class RedeemedTransactionAdmin(admin.ModelAdmin):
    list_display            = ('user', 'reference', 'amount', 'timestamp',)
    readonly_fields         = ('id', 'user', 'reference', 'amount', 'timestamp',)
    search_fields           = ('user__email', 'user__username', 'user__ip_address', 'user__id', 'reference', 'mode',)
    list_filter             = ('timestamp', 'mode',)

    fieldsets               = (
        (None, {'fields': ('mode',)}),
        ('Read-Only', {'fields': ('id', 'user', 'reference', 'amount', 'timestamp',)}),
    )


# Model Registrations
admin.site.register(Wallet, WalletAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(RedeemedTransaction, RedeemedTransactionAdmin)