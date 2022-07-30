from django.db import models
from django.conf import settings


TRANSACTION_TYPE            = (
    ('DP', 'Deposit'),
    ('WD', 'Withdrwal'),
    ('UP', 'Upgrade'),
)

CONTRACT                    = (
    ('Tier 1', 15/100),
    ('Tier 2', 20/100),
    ('Tier 3', 25/100),
)


class Wallet(models.Model):
    user                    = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wallet_user")
    balance                 = models.FloatField(default=0.00)
    profit                  = models.FloatField(default=0.00)
    contract                = models.CharField(max_length=10, choices=CONTRACT)

    class Meta:
        verbose_name        = "Wallet"
        verbose_name_plural = "Wallets"
    
    # Named Representation
    def __str__(self):
        return self.user.username
    

class Transaction(models.Model):
    mode                    = models.CharField(max_length=10, choices=TRANSACTION_TYPE)
    amount                  = models.FloatField(default=0.00)
    description             = models.TextField()
    

    timestamp               = models.DateTimeField(auto_now_add=True)
    status                  = models.BooleanField(default=False)
    reference               = models.SlugField(unique=True)

    class Meta:
        verbose_name        = "Transaction"
        verbose_name_plural = "Transactions"

    # Named Representation
    def __str__(self):
        return f'{self.mode} | {self.reference}'


class RedeemTransaction(models.Model):
    reference               = models.CharField(max_length=400)
    
    timestamp               = models.DateTimeField(auto_now_add=True)
    confirmed               = models.BooleanField(default=False)
    
    class Meta:
         pass