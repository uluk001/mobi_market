from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_filter = ('price',)
    list_display = ('title',)

admin.site.register(Product, ProductAdmin)