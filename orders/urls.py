from django.urls import path

from .views import *

app_name = 'orders'
urlpatterns = [
    path("cart/", CartView.as_view(), name="cart"),
    path("<int:cart_item_id>/edit_cart/", edit_cart_item, name="edit_cart_item"),
    path("<int:cart_item_id>/delete/", delete_cart_item, name="delete_cart_item"),

]