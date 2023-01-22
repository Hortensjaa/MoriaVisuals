from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView

from .forms import CustomerCreationForm


class SignUpView(CreateView):
    form_class = CustomerCreationForm
    success_url = reverse_lazy("login")
    template_name = "customers/signup.html"
