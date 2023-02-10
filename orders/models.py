from django.contrib import admin
from django.core.validators import RegexValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from phonenumbers import phonenumberutil
from phonenumbers.phonenumberutil import format_number


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
    phone_number = PhoneNumberField(null=False, blank=False)

    def __str__(self):
        return self.city + ' ' + self.street

    def formatted_phone(self):
        return format_number(self.phone_number, phonenumberutil.PhoneNumberFormat.INTERNATIONAL)


# order model; order is associated to customer and address
class Order(models.Model):
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    payed = models.BooleanField(default=False)

    @admin.display(description='Value', )
    def order_total_value(self):  # total value of order
        items = self.order_items.values_list('count', 'product__product__price')
        if len(items) > 0:
            sum_val = 0
            for item in items:
                sum_val += item[0] * item[1]
            return sum_val
        return None


# single item (ProductStore - product with size - and count) in order; similar to CartItem
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey('products.ProductStore', on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)

    def total_value(self):
        sum = self.count * self.product.product.price
        return sum
