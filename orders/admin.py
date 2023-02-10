from django.contrib import admin

from .models import *


class OrderInLine(admin.TabularInline):
    model = Order
    readonly_fields = ('customer', 'order_date', 'order_total_value')
    extra = 0


class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    extra = 0


class AddressAdmin(admin.ModelAdmin):
    inlines = [OrderInLine]
    list_display = ('city', 'postcode', 'street', 'number1', 'number2')


class OrderAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Customer', {'fields': ['customer']}),
        ('Address', {'fields': ['address']}),
        ('Payment status', {'fields': ['payed']}),
    ]
    readonly_fields = ('order_date', 'order_total_value')
    inlines = [OrderItemInLine]
    list_display = ('customer', 'order_date', 'order_total_value', 'payed')
    list_display_links = ('customer', )
    list_filter = ['order_date', 'payed']
    search_fields = ['customer']


admin.site.register(Order, OrderAdmin)
admin.site.register(Address, AddressAdmin)
