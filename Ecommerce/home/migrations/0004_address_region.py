# Generated by Django 5.1.4 on 2025-02-18 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_wallet_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='region',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
