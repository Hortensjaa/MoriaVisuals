from django import forms
from .models import CartItem


class CartItemEditForm(forms.ModelForm):

    class Meta:
        model = CartItem
        fields = ('count', )
