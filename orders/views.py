from datetime import datetime, timedelta

from django.core import mail
from django.conf import settings
import smtplib
import ssl
from email.message import EmailMessage
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView

from .forms import AddressForm
from carts.models import CartItem
from .models import *


# entering address to order
class EnterAddressView(CreateView):
    form_class = AddressForm
    template_name = "orders/enter_address.html"

    def form_valid(self, form):
        customer = self.request.user
        self.address = form.save()
        if Address.objects.filter(customer=customer):
            Address.objects.get(customer=customer).delete()
        customer.address = self.address
        customer.save()
        self.success_url = reverse_lazy('orders:order_confirmed', kwargs={'address_id': self.address.pk})
        return super().form_valid(form)


# if customer had placed an order before, his address is already saved in database;
# then, it's only needed to be confirmed up-to-date
def confirm_address(request):
    customer = request.user
    if customer.address is None or customer.address == '':
        return redirect('orders:enter_address')
    else:
        return render(request, 'orders/confirm_address.html', {'address': customer.address})


# sending a confirmation email after successful placing an order
def send_confirmation_email(order, customer):
    products_list = [
        str(item[0]) + ' x' + str(item[1]) + '\n'
        for item in order.order_items.values_list('product__product__name', 'count')
    ]
    msg = EmailMessage()
    msg.set_content(
        f"Hi {customer}!\n"
        f"Thank you for placing order no {order.id} with: \n{''.join(products_list)}"
        f"Estimated delivery time is {(order.order_date + timedelta(days=3)).date()}."
        f"If you have any questions, contact us by this email address."
    )
    msg["Subject"] = "Your Moria order confirmation"
    msg["From"] = "Moria Visuals"
    msg["To"] = customer.email

    context = ssl.create_default_context()

    with smtplib.SMTP(settings.EMAIL_HOST, port=settings.EMAIL_PORT) as smtp:
        smtp.starttls(context=context)
        smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        smtp.send_message(msg)


# view after successfully placing an order
def order_confirmed(request, address_id):
    customer = request.user
    address = Address.objects.get(id=address_id)
    order = Order.objects.create(address=address, customer=customer)
    products_in_cart = CartItem.objects.select_related().filter(customer=customer)
    if products_in_cart:
        for item in products_in_cart:
            OrderItem.objects.create(count=item.count, product=item.product, order=order)
            item.delete()
    customer.last_purchase = datetime.now()
    customer.save()
    send_confirmation_email(order, customer)
    return render(request, 'orders/order_confirmed.html', {'customer': customer})
