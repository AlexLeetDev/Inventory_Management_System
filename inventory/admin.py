from django.contrib import admin
from .models import Product, Supplier, Customer, Order

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

# Register the Customer model
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')  # Display customer name
    search_fields = ('first_name', 'last_name')  # Enable search by customer name

# Register the Order model
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer', 'date_ordered')  # Display product, customer, and order date
    search_fields = ('product__name', 'customer__first_name', 'customer__last_name')  # Enable search by product and customer names
    date_hierarchy = 'date_ordered'  # Date navigation for browsing orders by date