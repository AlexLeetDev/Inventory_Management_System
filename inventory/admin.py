from django.contrib import admin
from .models import Product, Supplier, Order

# Register the Product model
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')  # Display basic product info
    search_fields = ('name',)  # Search by product name
    list_filter = ('stock',)  # Simple filter for stock level

# Register the Supplier model
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Display supplier name
    search_fields = ('name',)  # Search by supplier name

# Register the Order model
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('product', 'supplier', 'date_ordered')  # Display product, supplier, and order date
    search_fields = ('product__name', 'supplier__name')  # Enable search by product and supplier name
    date_hierarchy = 'date_ordered'  # Date navigation for browsing orders by date