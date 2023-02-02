from django import forms
from .models import CartItem


# editing number of items corresponding to one product (ProductStore) you want to order
class CartItemEditForm(forms.ModelForm):

    class Meta:
        model = CartItem
        fields = ('count', )
