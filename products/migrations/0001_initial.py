# Generated by Django 4.1.5 on 2023-01-22 12:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Produkt', max_length=50)),
                ('description', models.TextField(default='Opis produktu', max_length=250)),
                ('price', models.PositiveIntegerField(default=200)),
                ('photo', models.ImageField(blank=True, upload_to='')),
                ('type', models.CharField(choices=[('Tee', 'Tee'), ('Sweatshirt', 'Sweatshirt'), ('Accessory', 'Accessory')], default=('Tee', 'Tee'), max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ProductStore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(choices=[('S', 'S'), ('M', 'M'), ('L', 'L'), ('U', 'universal')], default=('U', 'universal'), max_length=10)),
                ('count', models.PositiveIntegerField(default=10)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='available_sizes', to='products.product')),
            ],
        ),
    ]
