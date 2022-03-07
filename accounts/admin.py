from django.contrib import admin
from . import models

# Register your models here.

class Accountsadmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'owner',  'approved', 'is_avalabile')
    list_display_links = ('title', 'price', 'owner')
    filter_horizontal = ()
    list_filter = ['approved', 'is_avalabile']
    fieldsets = ()

admin.site.register(models.Review)
admin.site.register(models.Accounts, Accountsadmin)
admin.site.register(models.Trade_Requests)