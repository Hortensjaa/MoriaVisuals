from django.db.models import F, Sum
from django.shortcuts import render, redirect
from django.utils.datetime_safe import datetime
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response

from products.views import make_url
from .models import *
from .forms import CartItemEditForm


class CartView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'carts/cart.html'

    def get(self, request):
        if request.user.is_authenticated:
            customer = request.user
            if customer.cart:
                cart = customer.cart.annotate(product_id=F('product__product__id'),
                                              id=F('id'),
                                              size=F('product__size'),
                                              price=F('product__product__price'),
                                              sum_item=F('price') * F('count'))
                for product in cart:
                    product['url'] = make_url(product['product_id'])
                summary = cart.aggregate(sum=Sum('sum_item'), number_of_items=Sum('count'))
                return Response({'cart': cart, 'summary': summary})
            #TODO: Niewyswietlanie pustego koszyka XD
            return Response({'text': 'Jeszcze nie masz nic w swoim koszyku'})
        return Response({'text': 'Zaloguj się, żeby dodać rzecz do koszyka'})


def delete_cart_item(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.delete()
    return redirect('carts:cart')


def edit_cart_item(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    form = CartItemEditForm(instance=cart_item)
    if request.method == 'POST':
        form = CartItemEditForm(request.POST, instance=cart_item)
        if form.is_valid():
            form.save()
            return redirect('carts:cart')
    return render(request, 'carts/edit_cart_item.html', {'form': form, 'cart_item_id': cart_item_id})
