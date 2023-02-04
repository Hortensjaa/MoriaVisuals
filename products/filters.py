import django_filters
from django import forms

from .models import Product


# filter on home page with all products
class ProductFilter(django_filters.FilterSet):
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['type']
        form = forms.Form
