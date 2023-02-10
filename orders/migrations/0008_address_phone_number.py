# Generated by Django 4.1.5 on 2023-02-05 17:08

import phonenumber_field.modelfields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_rename_prepayed_order_payed'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(default='+48123456789', max_length=128, region=None),
        ),
    ]
