import django_filters
from django import forms

from .models import Product
from .types_and_sizes import TYPES


# filter on home page with all products
class ProductFilter(django_filters.FilterSet):
    price__lte = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    price__gte = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    name = django_filters.CharFilter(lookup_expr='icontains')
    type = django_filters.MultipleChoiceFilter(field_name='type', choices=TYPES, widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Product
        fields = []
        form = forms.Form
