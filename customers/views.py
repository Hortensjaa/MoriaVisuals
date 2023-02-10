from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView

from orders.models import Address, Order

from .forms import CustomerCreationForm


# TODO: customer profile with orders summarize, address etc.
# signing up - creating new customer
class SignUpView(CreateView):
    form_class = CustomerCreationForm
    success_url = reverse_lazy("login")
    template_name = "customers/signup.html"


# all customer's personal info and delivery address
def customer_profile(request):
    customer = request.user
    contact = Address.objects.get(customer=customer)


# all customer's orders with filters
def customer_orders(request):
    customer = request.user
    orders = Order.objects.filter(customer=customer).order_by('order_date')
    return render(request, 'customers/customer_orders.html', {'orders': orders})

