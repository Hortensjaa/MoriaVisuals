# Generated by Django 4.1.5 on 2023-01-23 15:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_address_postcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='postcode',
            field=models.CharField(max_length=6, validators=[django.core.validators.RegexValidator(message='Postcode must be in the format "dd-ddd".', regex='^\\d{2}-\\d{3}$')]),
        ),
    ]
