# Generated by Django 4.0.6 on 2022-08-01 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallet',
            name='btc_address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='wallet',
            name='eth_address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='wallet',
            name='usdt_address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
