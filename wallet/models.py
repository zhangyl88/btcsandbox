from django.db import models
from django.conf import settings

from btcsandbox import settings as _settings


_TYPE                        = (
    ('DP', 'Deposit'),
    ('WD', 'Withdrwal'),
    ('UP', 'Upgrade'),
)

_CONTRACT                    = (
    ('LV1', 'Level 1'),
    ('LV2', 'Level 2'),
    ('LV3', 'Level 3'),
)

_MODE                       = (
    ('BTC', 'Bitcoin'),
    ('USDT', 'Tether USD'),
    ('ETH', 'Ethereum'),
)


class Wallet(models.Model):
    user                    = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wallet_user")
    referrals               = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="wallet_referrals", blank=True)

    balance                 = models.FloatField(default=0.00)
    profit                  = models.FloatField(default=0.00)
    r_balance               = models.FloatField(default=0.00)
    
    level                   = models.CharField(max_length=10, choices=_CONTRACT, default="LV1")

    # withdrawals
    btc_address             = models.CharField(max_length=200, blank=True, null=True)
    eth_address             = models.CharField(max_length=200, blank=True, null=True)
    usdt_address            = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name        = "Wallet"
        verbose_name_plural = "Wallets"
        
    def update_r_balance(self):
        self.r_balance += _settings.REFERRAL_REWARD
        self.save()
    
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
        verbose_name        = "Transaction"
        verbose_name_plural = "Transactions"

    # Named Representation
    def __str__(self):
        return f'{self.mode}{self.reference}'


class RedeemedTransaction(models.Model):
    user                    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="rt_user")
    amount                  = models.FloatField(default=0.00)
    
    reference               = models.CharField(max_length=400)
    mode                    = models.CharField(max_length=5, choices=_MODE)
    
    timestamp               = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = "Redeemed Transaction"
        verbose_name_plural = "Redeemed Transactions"

    # Named Representation
    def __str__(self):
        return f'{self.mode}{self.reference}'