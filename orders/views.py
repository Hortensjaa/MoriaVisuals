from datetime import datetime

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import AddressForm
from carts.models import CartItem
from .models import *


class EnterAddressView(CreateView):
    form_class = AddressForm
    template_name = "orders/enter_address.html"

    def form_valid(self, form):
        self.object = form.save()
        self.success_url = reverse_lazy('orders:order_confirmed', kwargs={'address_id': self.object.pk})
        return super().form_valid(form)


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
    return render(request, 'orders/order_confirmed.html')
