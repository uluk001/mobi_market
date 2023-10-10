from django.contrib import admin
from .models import Product, AdditionalImage


class AdditionalImageInline(admin.TabularInline):
    model = AdditionalImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_filter = ('price',)
    list_display = ('title',)
    inlines = [AdditionalImageInline]

admin.site.register(Product, ProductAdmin)
