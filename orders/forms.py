from django.forms import ModelForm

from .models import *


class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
