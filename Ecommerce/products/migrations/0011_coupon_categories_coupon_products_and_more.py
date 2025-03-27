# Generated by Django 5.1.4 on 2025-02-09 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_product_coupons'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='category_coupons', to='products.category'),
        ),
        migrations.AddField(
            model_name='coupon',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='product_coupons', to='products.product'),
        ),
        migrations.AlterField(
            model_name='product',
            name='coupons',
            field=models.ManyToManyField(related_name='coupon_products', to='products.coupon'),
        ),
    ]
