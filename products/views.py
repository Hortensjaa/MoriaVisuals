from urllib.parse import urlunparse

from django.db.models import Value, Q, F, URLField, Case, When, IntegerField, Sum
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.urls import reverse

from .models import *
from carts.models import CartItem


def make_url(product_id):
    url = urlunparse(('http', '127.0.0.1:8000', f'{product_id}/', '', '', ''))
    return url.replace(' ', '%20')


#TODO: dodanie filtrów po typie, cenie itd
class HomePageView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'products/products_list.html'

    def get(self, request):
        products = Product.objects.values('name', 'price', 'id') \
            .alias(count_all=Sum('available_sizes__count')).filter(count_all__gt=0)
        for product in products:
            product['url'] = make_url(product['id'])
        return Response({'products': products})


def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/product_details.html', {'product': product, 'sizes': product.available_sizes.all})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    selected_size = product.available_sizes.get(pk=request.POST['size'])
    selected_size.count -= 1
    selected_size.save()

    if request.user.is_authenticated:
        customer = request.user
        product_in_cart = CartItem.objects.select_related()\
            .filter(customer=customer, product=selected_size)
        if product_in_cart:
            product_in_cart[0].count += 1
            product_in_cart[0].save()
        else:
            CartItem.objects.create(customer=customer, product=selected_size, count=1)

    return HttpResponseRedirect(reverse('carts:cart'))
