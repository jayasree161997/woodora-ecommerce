# Generated by Django 5.1.4 on 2025-02-13 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_categoryoffer_productoffer_referraloffer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('COD', 'Cash on Delivery'), ('RAZORPAY', 'Razorpay')], max_length=100),
        ),
    ]
