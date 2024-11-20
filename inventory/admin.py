from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Supplier, Customer, Order, Inventory, ActivityLog

# Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('icon', 'name', 'price', 'featured', 'supplier')
    list_editable = ('featured',)  # Allow inline editing for the 'featured' field
    list_filter = ('featured', 'supplier')  # Add filters for featured and supplier

    def icon(self, obj):
        return format_html('<i class="fa-sharp-duotone fa-box" style="--fa-primary-color: #D2691E; --fa-secondary-color: #B8860B;"></i>')
    icon.short_description = ''


# Supplier Admin
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('icon', 'name')

    def icon(self, obj):
        return format_html('<i class="fa-sharp-duotone fa-truck" style="--fa-primary-color: red;"></i>')
    icon.short_description = ''


# Customer Admin
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('icon', 'first_name', 'last_name')

    def icon(self, obj):
        return format_html('<i class="fa-sharp-duotone fa-user" style="--fa-primary-color: green;"></i>')
    icon.short_description = ''


# Order Admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('icon', 'product', 'customer', 'date_ordered')

    def icon(self, obj):
        return format_html('<i class="fa-sharp-duotone fa-cart-shopping" style="--fa-primary-color: orange;"></i>')
    icon.short_description = ''


# Inventory Admin
@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('icon', 'product', 'stock_level')

    def icon(self, obj):
        return format_html('<i class="fa-sharp-duotone fa-warehouse" style="--fa-primary-color: blue;"></i>')
    icon.short_description = ''


# ActivityLog Admin
@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('icon', 'description', 'timestamp')

    def icon(self, obj):
        return format_html('<i class="fa-sharp-duotone fa-clipboard-list" style="--fa-primary-color: purple;"></i>')
    icon.short_description = ''