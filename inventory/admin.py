from django.contrib import admin
from .models import Product, Supplier, Customer, Order

# Inline model to display related orders on Product and Customer pages
class OrderInline(admin.TabularInline):
    model = Order
    extra = 0  # Display without extra blank rows

# Register the Product model with custom display options and inline orders
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_type', 'price', 'stock')  # Display product fields
    search_fields = ('name',)  # Enable search functionality by product name
    list_filter = ('product_type', 'price')  # Filter options for product type and price
    ordering = ('product_type', 'name')  # Sort by product type, then by name
    inlines = [OrderInline]  # Display related orders inline

    # Custom action to mark selected products as out of stock
    actions = ['mark_out_of_stock']

    def mark_out_of_stock(self, request, queryset):
        """Custom action to mark selected products as out of stock"""
        updated_count = queryset.update(stock=0)
        self.message_user(request, f"{updated_count} products marked as out of stock.")
    mark_out_of_stock.short_description = "Mark selected products as out of stock"

# Register the Supplier model with basic display options
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Display supplier name
    search_fields = ('name',)  # Enable search functionality by supplier name

# Register the Customer model with custom display options and inline orders
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')  # Display customer names
    search_fields = ('first_name', 'last_name')  # Enable search functionality by customer name
    inlines = [OrderInline]  # Display related orders inline

# Register the Order model with date hierarchy and custom options
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer', 'date_ordered')  # Display product, customer, and order date
    search_fields = ('product__name', 'customer__first_name', 'customer__last_name')  # Enable search by product/customer names
    list_filter = ('date_ordered',)  # Add filter for order date
    date_hierarchy = 'date_ordered'  # Date navigation bar for easier order browsing by date