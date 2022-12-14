# Generated by Django 4.0.6 on 2022-08-01 10:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.FloatField(default=0.0)),
                ('profit', models.FloatField(default=0.0)),
                ('r_balance', models.FloatField(default=0.0)),
                ('level', models.CharField(choices=[('LV1', 'Level 1'), ('LV2', 'Level 2'), ('LV3', 'Level 3')], default='LV1', max_length=10)),
                ('referrals', models.ManyToManyField(blank=True, related_name='wallet_referrals', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='wallet_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Wallet',
                'verbose_name_plural': 'Wallets',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0.0)),
                ('transaction_type', models.CharField(choices=[('DP', 'Deposit'), ('WD', 'Withdrwal'), ('UP', 'Upgrade')], max_length=5)),
                ('description', models.TextField(blank=True, default=models.CharField(choices=[('DP', 'Deposit'), ('WD', 'Withdrwal'), ('UP', 'Upgrade')], max_length=5), null=True)),
                ('mode', models.CharField(choices=[('BTC', 'Bitcoin'), ('USDT', 'Tether USD'), ('ETH', 'Ethereum')], max_length=5)),
                ('status', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('reference', models.SlugField(unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tr_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
            },
        ),
        migrations.CreateModel(
            name='RedeemedTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0.0)),
                ('reference', models.CharField(max_length=400)),
                ('mode', models.CharField(choices=[('BTC', 'Bitcoin'), ('USDT', 'Tether USD'), ('ETH', 'Ethereum')], max_length=5)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rt_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Redeemed Transaction',
                'verbose_name_plural': 'Redeemed Transactions',
            },
        ),
    ]
