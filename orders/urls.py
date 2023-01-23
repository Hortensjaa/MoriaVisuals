from django.urls import path

from .views import *

app_name = 'orders'
urlpatterns = [
    path("address/", EnterAddressView.as_view(), name="enter_address"),
    path("confirm_address/", confirm_address, name="confirm_address"),
    path("confirm/<int:address_id>", order_confirmed, name="order_confirmed"),
]
