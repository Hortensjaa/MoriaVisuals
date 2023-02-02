from datetime import datetime

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


# TODO: sending confirmation emails
# view after successfully placing an order
def order_confirmed(request, address_id):
    customer = request.user
    address = Address.objects.get(id=address_id)
    order = Order.objects.create(address=address, customer=customer)
    product_in_cart = CartItem.objects.select_related().filter(customer=customer)
    if product_in_cart:
        OrderItem.objects.create(count=product_in_cart[0].count, product=product_in_cart[0].product, order=order)
        product_in_cart[0].delete()
    customer.last_purchase = datetime.now()
    customer.save()
    return render(request, 'orders/order_confirmed.html', {'customer': customer})
