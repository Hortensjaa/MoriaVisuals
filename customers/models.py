from django.db import models
from django.db.models import F
from django.contrib.auth.models import AbstractUser
from carts.models import CartItem


# customer model; email is required for confirmation email sending purposes
class Customer(AbstractUser):
    username = models.CharField(max_length=30, unique=False)
    email = models.EmailField(max_length=255, unique=True)
    USERNAME_FIELD = 'email'  # email is treated as required username field
    REQUIRED_FIELDS = ['username']
    last_purchase = models.DateTimeField(blank=True, null=True)
    # customer can have address already saved in database
    address = models.ForeignKey('orders.Address', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        if self.first_name:
            return self.first_name
        return self.email

    @property  # every customer has his/hers cart
    def cart(self):
        cart = CartItem.objects.filter(customer=self)
        cart = cart.annotate(name=F('product__product__name')).values('name', 'count')
        return cart
