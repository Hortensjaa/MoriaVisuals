import django_filters
from django import forms

from .models import Product
from .types_and_sizes import TYPES


# filter on home page with all products
class ProductFilter(django_filters.FilterSet):
    # minimum price
    price__gte = django_filters.NumberFilter(
        field_name='price', lookup_expr='gte',
        widget=forms.NumberInput(attrs={'placeholder': 'min', 'min': 0, 'max': 1000, 'step': 50})
    )
    # maximum price
    price__lte = django_filters.NumberFilter(
        field_name='price', lookup_expr='lte',
        widget=forms.NumberInput(attrs={'placeholder': 'max', 'min': 0, 'max': 1000, 'step': 50}))
    name = django_filters.CharFilter(lookup_expr='icontains')
    type = django_filters.MultipleChoiceFilter(field_name='type', choices=TYPES, widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Product
        fields = []
        form = forms.Form
