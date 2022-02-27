from django.contrib import admin
from . import models
from .models import Payment, Order, OrderProduct
# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id',)

class CartitemAdmin(admin.ModelAdmin):
    list_display = ('account_id', 'cart_id')



admin.site.register(models.Cart, CartAdmin)
admin.site.register(models.CartItem, CartitemAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'order_total', 'tax', 'status', 'is_ordered', 'created_at']


admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)