from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from carts.models import CartItem
from .forms import CustomerCreationForm, CustomerChangeForm
from .models import *


class CartAdmin(admin.TabularInline):
    model = CartItem
    extra = 0


class CustomerAdmin(UserAdmin):
    add_form = CustomerCreationForm
    form = CustomerChangeForm
    model = Customer
    list_display = ["email", "first_name", "last_name", "is_staff"]
    ordering = ("-is_staff", "last_name",)
    fieldsets = ((None, {"fields": ("username", "password")}),
                 ("Personal info", {"fields": ("first_name", "last_name", "email")}),
                 ("Important dates", {"fields": ("last_login", "date_joined", "last_purchase")}),
                 ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "user_permissions",),
                                  "classes": ['collapse']}),)
    add_fieldsets = ((None, {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"), },),)
    inlines = [CartAdmin]


admin.site.register(Customer, CustomerAdmin)
