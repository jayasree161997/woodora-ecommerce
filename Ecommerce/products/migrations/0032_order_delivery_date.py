# Generated by Django 5.1.4 on 2025-03-12 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0031_product_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
