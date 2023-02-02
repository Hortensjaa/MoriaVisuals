from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Customer


# creating new customer
class CustomerCreationForm(UserCreationForm):

    class Meta:
        model = Customer
        fields = ("email",)


# changing customer's email
class CustomerChangeForm(UserChangeForm):

    class Meta:
        model = Customer
        fields = ("email",)
