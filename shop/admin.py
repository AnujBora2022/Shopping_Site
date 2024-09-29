from django.contrib import admin

# Register your models here.
from .models import Category, Product, Order

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_trending')  # Add is_trending to the list display
    list_filter = ('is_trending',)  # Filter products by trending status
    search_fields = ('name',)  # Allow searching by product name

admin.site.register(Product, ProductAdmin)

admin.site.register(Category)
admin.site.register(Order)
