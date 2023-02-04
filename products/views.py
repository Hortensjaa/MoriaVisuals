from datetime import datetime
from urllib.parse import urlunparse

from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.urls import reverse

from .models import *
from .filters import ProductFilter
from carts.models import CartItem


# function making url on site FIXME: this is not a good one XD
def make_url(product_id):
    url = urlunparse(('http', '127.0.0.1:8000', f'{product_id}/', '', '', ''))
    return url.replace(' ', '%20')


# home page view - all products with they name, photos and prices
class HomePageView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'products/products_list.html'

    def get(self, request):
        products = Product.objects.alias(count_all=Sum('available_sizes__count')).filter(count_all__gt=0)
        filter = ProductFilter(request.GET, queryset=products)
        return Response({'filter': filter})


# detail view on single product (available sizes, description etc.)
def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/product_details.html', {'product': product, 'sizes': product.available_sizes.all})


# adding product (in detail view) to customer's cart
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    # size needs to be selected by user
    selected_size = product.available_sizes.get(pk=request.POST['size'])
    # number of available items of this product with selected size decrease by one, when customer add it to cart
    selected_size.count -= 1
    selected_size.save()
    # only authenticated user can add product (ProductStore item) to cart
    if request.user.is_authenticated:
        customer = request.user
        product_in_cart = CartItem.objects.select_related()\
            .filter(customer=customer, product=selected_size)
        # if this ProductStore item (product with size) is already in cart, count of corresponding CartItem increase +1
        if product_in_cart:
            product_in_cart[0].count += 1
            product_in_cart[0].save()
        # else, new CartItem object is created and linked to the user
        else:
            CartItem.objects.create(customer=customer, product=selected_size, count=1)

    return HttpResponseRedirect(reverse('carts:cart'))
