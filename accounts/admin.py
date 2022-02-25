from django.contrib import admin
from . import models

# Register your models here.

class Accountsadmin(admin.ModelAdmin):
    list_display = ('title', 'account_img','price', 'owner','options', 'category','is_avalabile')
    list_display_links = ('title', 'price', 'owner')


admin.site.register(models.Review)
admin.site.register(models.Accounts, Accountsadmin)