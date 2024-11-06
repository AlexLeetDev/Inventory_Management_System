from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Product, Supplier, Customer, Order  # Import your models

# Register the Product model with custom display options
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')  # Customize which fields are displayed in the list view
    search_fields = ('name',)  # Enable search functionality by product name
    list_filter = ('price',)  # Add a filter option for price

# Register the Supplier model
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Display supplier name
    search_fields = ('name',)  # Enable search functionality by supplier name

# Register the Customer model
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')  # Display first and last names
    search_fields = ('first_name', 'last_name')  # Enable search functionality

# Register the Order model
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer', 'date_ordered')  # Display product, customer, and order date
    search_fields = ('product__name', 'customer__first_name', 'customer__last_name')  # Enable search on product name and customer names
    list_filter = ('date_ordered',)  # Add a filter option for the order date
