# Generated by Django 5.1.4 on 2025-01-24 16:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Category Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Category Description')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Product Name')),
                ('description', models.TextField(verbose_name='Product Description')),
                ('brand', models.CharField(blank=True, max_length=100, null=True, verbose_name='Brand')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price')),
                ('quantity', models.IntegerField()),
                ('original_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Original Price')),
                ('discount_percentage', models.IntegerField(blank=True, null=True, verbose_name='Discount Percentage')),
                ('stock_status', models.BooleanField(default=True, verbose_name='In Stock')),
                ('sold', models.PositiveIntegerField(default=0, verbose_name='Units Sold')),
                ('main_image', models.ImageField(default='products/main_images/default.jpg', upload_to='products/main_images/', verbose_name='Main Image')),
                ('material', models.CharField(blank=True, max_length=100, null=True, verbose_name='Material')),
                ('dimensions', models.CharField(blank=True, max_length=100, null=True, verbose_name='Dimensions')),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Weight (kg)')),
                ('warranty', models.CharField(blank=True, max_length=100, null=True, verbose_name='Warranty')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.category', verbose_name='Category')),
            ],
        ),
        migrations.CreateModel(
            name='ProductThumbnail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='products/thumbnails', verbose_name='Thumbnail Image')),
                ('alt_text', models.CharField(blank=True, max_length=100, null=True, verbose_name='Alt Text')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thumbnails', to='products.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='thumbnail_images',
            field=models.ManyToManyField(related_name='product_thumbnails', to='products.productthumbnail', verbose_name='Thumbnail Images'),
        ),
        migrations.CreateModel(
            name='ProductVariant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variant_name', models.CharField(max_length=50)),
                ('variant_value', models.CharField(blank=True, max_length=50, null=True)),
                ('color_image', models.ImageField(upload_to='products/color_variants', verbose_name='Color Image')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='products.product')),
            ],
        ),
    ]
