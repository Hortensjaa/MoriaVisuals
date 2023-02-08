from django.urls import path

from .views import *

app_name = 'customer'
urlpatterns = [
    path("my_orders/", customer_orders, name="customer_orders"),
]
