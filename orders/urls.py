from django.urls import path

from .views import *

app_name = 'orders'
urlpatterns = [
    path("address/", EnterAddressView.as_view(), name="enter_address"),
    path("confirm_address/", confirm_address, name="confirm_address"),
    path('payment/<int:address_id>', process_payment, name='process_payment'),
    path('paypal-cancel/', PaypalCancelView.as_view(), name='payment_cancelled'),
    path("confirm/<int:order_id>", order_confirmed, name="order_confirmed"),
]
