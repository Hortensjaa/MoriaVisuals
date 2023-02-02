from django.db import models
from django.db.models import F
from django.contrib.auth.models import AbstractUser
from carts.models import CartItem


class Customer(AbstractUser):
    username = models.CharField(max_length=30, unique=False)
    email = models.EmailField(max_length=255, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    last_purchase = models.DateTimeField(blank=True, null=True)
    address = models.ForeignKey('orders.Address', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        if self.first_name:
            return self.first_name
        return self.email

    @property
    def cart(self):
        cart = CartItem.objects.filter(customer=self)
        cart = cart.annotate(name=F('product__product__name')).values('name', 'count')
        return cart
