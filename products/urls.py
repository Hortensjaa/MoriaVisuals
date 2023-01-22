from django.urls import path

from .views import *

app_name = 'products'
urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('<int:product_id>/', detail, name='detail_view'),
    path("<int:product_id>/add_to_cart/", add_to_cart, name="add_to_cart"),
]
