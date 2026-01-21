from django.contrib import admin
from .models import Order, OrderItem, ShippingAddress


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ('product', 'price', 'user')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'amount_paid', 'date_ordered',)
    search_fields = ('email',)
    inlines =  [OrderItemInline]
    readonly_fields = ('amount_paid',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'price',)
    search_fields = ('product',)


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('country', 'state', 'city', 'address2', 'address1')
    list_filter = ('country', 'state', 'city')
    search_fields = ('user', 'city', 'address2', 'address1')
    ordering  = ('city',)    
