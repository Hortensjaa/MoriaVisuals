from datetime import datetime, timedelta
import smtplib
import ssl

from _decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
from email.message import EmailMessage

from django.views.generic import FormView, TemplateView
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView

from .forms import AddressForm
from carts.models import CartItem
from .models import *
from MoriaVisuals.settings import PAYPAL_RECEIVER_EMAIL


# DELIVERY ADDRESS
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
        self.success_url = reverse_lazy('orders:process_payment', kwargs={'address_id': self.address.pk})
        return super().form_valid(form)


# if customer had placed an order before, his address is already saved in database;
# then, it's only needed to be confirmed up-to-date
def confirm_address(request):
    customer = request.user
    if customer.address is None or customer.address == '':
        return redirect('orders:enter_address')
    else:
        return render(request, 'orders/confirm_address.html', {'address': customer.address})


# making an order
def make_order(request, address_id):
    customer = request.user
    address = get_object_or_404(Address, id=address_id)
    order = Order.objects.create(address=address, customer=customer)
    products_in_cart = CartItem.objects.select_related().filter(customer=customer)
    if products_in_cart:
        for item in products_in_cart:
            OrderItem.objects.create(count=item.count, product=item.product, order=order)
            item.delete()
    return order


# PAYMENT
# served with PayPal
def process_payment(request, address_id):
    order = make_order(request, address_id)

    paypal_dict = {
        'business': PAYPAL_RECEIVER_EMAIL,
        'amount': f"{order.order_total_value()}.00",
        'item_name': 'Order {}'.format(order.id),
        'invoice': str(order.id),
        'currency_code': 'PLN',
        'notify_url': request.build_absolute_uri(reverse('paypal-ipn')),
        'return_url': request.build_absolute_uri(reverse('orders:order_confirmed', kwargs={'order_id': order.id})),
        'cancel_return': request.build_absolute_uri(reverse('orders:payment_cancelled')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'orders/paypal_form.html', {'order': order, 'form': form})


class PaypalCancelView(TemplateView):
    template_name = 'orders/paypal_cancel.html'


# ORDER CONFIRMATION
# sending a confirmation email after successful placing an order
def send_confirmation_email(order, customer):
    products_list = [
        f"{item[0]} {item[1]}: {item[2]} zł x{item[3]}\n"
        for item in order.order_items.values_list(
            'product__product__name', 'product__size', 'product__product__price', 'count'
        )
    ]
    msg = EmailMessage()
    msg.set_content(
        f"Hi {customer}!\n"
        f"Thank you for placing order no {order.id} with: \n{''.join(products_list)}"
        f"Total value: {order.order_total_value()} zł.\n"
        f"Estimated delivery time is {(order.order_date + timedelta(days=3)).date()}. "
        f"If you have any questions, contact us by this email address or Instagram account."
    )
    msg["Subject"] = f"Your Moria order no {order.id}"
    msg["From"] = "Moria Visuals"
    msg["To"] = customer.email

    context = ssl.create_default_context()

    with smtplib.SMTP(settings.EMAIL_HOST, port=settings.EMAIL_PORT) as smtp:
        smtp.starttls(context=context)
        smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        smtp.send_message(msg)


# view after successfully placing an order
def order_confirmed(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.payed = True
    order.save()
    customer = request.user
    customer.last_purchase = datetime.now()
    customer.save()
    send_confirmation_email(order, customer)
    return render(request, 'orders/order_confirmed.html', {'customer': customer})
