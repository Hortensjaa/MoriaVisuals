import django_filters
from django import forms

from .models import Customer
from orders.models import Order


# filter on home page with all products
class OrdersFilter(django_filters.FilterSet):
    # minimum value
    price__gte = django_filters.NumberFilter(
        field_name='price', lookup_expr='gte',
        widget=forms.NumberInput(attrs={'placeholder': 'min', 'min': 0, 'max': 1000, 'step': 50})
    )
    # maximum value
    price__lte = django_filters.NumberFilter(
        field_name='price', lookup_expr='lte',
        widget=forms.NumberInput(attrs={'placeholder': 'max', 'min': 0, 'max': 1000, 'step': 50}))

    class Meta:
        model = Order
        fields = []
        form = forms.Form
