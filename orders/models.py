from django.db import models
from django.contrib import admin
from django.core.validators import RegexValidator


# address stored in database; address is associated with user
class Address(models.Model):
    city = models.CharField(max_length=20)
    street = models.CharField(max_length=20)
    number1 = models.PositiveIntegerField()  # building number
    number2 = models.PositiveIntegerField(blank=True, null=True)  # flat number
    # Polish postcode field
    postcode = models.CharField(
        max_length=6,
        validators=[RegexValidator(regex='^\d{2}-\d{3}$', message='Enter postcode in "dd-ddd" format.')]
    )

    def __str__(self):
        return self.city + ' ' + self.street


# order model; order is associated to customer and address
class Order(models.Model):
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)

    @admin.display(description='Value', )
    def order_value(self):  # total value of order
        items = self.order_items.values_list('count', 'product__product__price')
        if len(items) > 0:
            sum = 0
            for item in items:
                sum += item[0] * item[1]
            return sum
        return None


# single item (ProductStore - product with size - and count) in order; similar to CartItem
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey('products.ProductStore', on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)

    def value(self):
        sum = self.count * self.product.product.price
        return sum
