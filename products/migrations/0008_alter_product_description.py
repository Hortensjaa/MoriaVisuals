# Generated by Django 4.1.5 on 2023-02-08 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_product_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(default='Size chart (width/lenght):\n\nS - 50/60cm\n\nM - 55/71cm\n\nL - 60/77cm', max_length=5000),
        ),
    ]
