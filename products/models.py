from django.contrib import admin
from django.db import models

from .types_and_sizes import SIZES, TYPES


# model corresponding to product with its name, price etc.; doesn't contain size
# TODO: many photos of one product
class Product(models.Model):
    name = models.CharField(max_length=50, default='Some product')
    description = models.TextField(max_length=5000,
                                   default='Size chart (width/lenght):\n\nS - 50/60cm\n\nM - 55/71cm\n\nL - 60/77cm')
    price = models.PositiveIntegerField(default=200)
    photo = models.ImageField(blank=True, upload_to='photos')
    type = models.CharField(choices=TYPES, max_length=50, default=TYPES[0])  # t-shirts, accessories etc.

    def __str__(self):
        return self.name

    # admin displays' associated things
    @admin.display(description='price', )
    def price_string(self):
        return str(self.price) + ' zł'

    @admin.display(description='S', )
    def available_s(self):
        products = self.available_sizes.filter(size='S').values('count')
        if len(products) > 0:
            return products[0]['count']
        return None

    @admin.display(description='M', )
    def available_m(self):
        products = self.available_sizes.filter(size='M').values('count')
        if len(products) > 0:
            return products[0]['count']
        return None

    @admin.display(description='L', )
    def available_l(self):
        products = self.available_sizes.filter(size='L').values('count')
        if len(products) > 0:
            return products[0]['count']
        return None

    @admin.display(description='U', )
    def available_u(self):
        products = self.available_sizes.filter(size='U').values('count')
        if len(products) > 0:
            return products[0]['count']
        return None


# model corresponding to type of product in store with size and count (number of products with selected size available)
class ProductStore(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='available_sizes')
    size = models.CharField(choices=SIZES, max_length=10, default=SIZES[3])
    count = models.PositiveIntegerField(default=10)

    def __str__(self):
        return self.product.name + ': ' + self.size

    def is_available(self):
        return self.count != models.IntegerField(0)
