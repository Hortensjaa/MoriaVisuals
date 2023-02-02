from django.db import models


# item (product with size, so ProductStore model) in customer's cart with number of product you want to order
class CartItem(models.Model):
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, related_name='products_in_cart')
    product = models.ForeignKey('products.ProductStore', on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)
