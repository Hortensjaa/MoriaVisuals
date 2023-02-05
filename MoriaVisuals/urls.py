from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from customers.views import SignUpView

urlpatterns = [
                path('', include('products.urls')),
                path('cart/', include('carts.urls')),
                path('order/', include('orders.urls')),
                path('admin/', admin.site.urls),
                path("accounts/", include("django.contrib.auth.urls")),
                path("signup/", SignUpView.as_view(), name="signup"),
                path('paypal/', include('paypal.standard.ipn.urls')),
              ]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
