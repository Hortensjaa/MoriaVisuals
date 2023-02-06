from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView

from orders.models import Address
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

