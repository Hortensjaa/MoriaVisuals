from django.forms import ModelForm

from .models import *


# entering address to order
class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
