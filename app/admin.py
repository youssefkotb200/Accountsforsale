from django.contrib import admin
from . import models
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')


admin.site.register(models.Categories, CategoryAdmin)

# admin.site.register(models.Cart)
# admin.site.register(models.Trade_Requests)
# admin.site.register(models.Trade)
# admin.site.register(models.Transactions)

