from django.db import models
from django.conf import settings


_TYPE                        = (
    ('DP', 'Deposit'),
    ('WD', 'Withdrwal'),
    ('UP', 'Upgrade'),
)

_CONTRACT                    = (
    ('Tier 1', 15/100),
    ('Tier 2', 20/100),
    ('Tier 3', 25/100),
)

_MODE                = (
    ('BTC', 'Bitcoin'),
    ('USDT', 'Tether USD'),
    ('ETH', 'Ethereum'),
)


class Wallet(models.Model):
    user                    = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wallet_user")
    balance                 = models.FloatField(default=0.00)
    profit                  = models.FloatField(default=0.00)
    
    level                   = models.CharField(max_length=10, choices=_CONTRACT)

    class Meta:
        verbose_name        = "Wallet"
        verbose_name_plural = "Wallets"
    
    # Named Representation
    def __str__(self):
        return self.user.username
    

class Transaction(models.Model):
    user                    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tr_user")
    amount                  = models.FloatField(default=0.00)
    transaction_type        = models.CharField(max_length=5, choices=_TYPE)
    description             = models.TextField(blank=True, null=True, default=transaction_type)
    
    mode                    = models.CharField(max_length=5, choices=_MODE)

    status                  = models.BooleanField(default=False)
    
    timestamp               = models.DateTimeField(auto_now_add=True)
    reference               = models.SlugField(unique=True)

    class Meta:
        verbose_name        = "Deposit"
        verbose_name_plural = "Deposits"

    # Named Representation
    def __str__(self):
        return f'{self.mode} [{self.reference}]'


class RedeemedTransaction(models.Model):
    user                    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="rt_user")
    
    reference               = models.CharField(max_length=400)
    deposit_mode            = models.CharField(max_length=5, choices=_MODE)
    
    timestamp               = models.DateTimeField(auto_now_add=True)
    confirmed               = models.BooleanField(default=False)
    
    class Meta:
        verbose_name        = "Redeemed Transaction"
        verbose_name_plural = "Redeemed Transactions"

    # Named Representation
    def __str__(self):
        return f'{self.user.username} [{self.reference}]'