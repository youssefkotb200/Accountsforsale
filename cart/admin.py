from django.contrib import admin
from . import models
# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id',)

class CartitemAdmin(admin.ModelAdmin):
    list_display = ('account_id', 'cart_id')



admin.site.register(models.Cart, CartAdmin)
admin.site.register(models.CartItem, CartitemAdmin)