from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Supplier, Customer, Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('icon', 'name', 'price', 'stock')

    def icon(self, obj):
        # Set the primary color to blue for the box icon
        return format_html(
            '<i class="fa-sharp-duotone fa-box" style="--fa-primary-color: blue;"></i>'
        )
    icon.short_description = ''

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('icon', 'name')

    def icon(self, obj):
        # Set the primary color to red using inline style
        return format_html(
            '<i class="fa-duotone fa-truck" style="--fa-primary-color: red;"></i>'
        )
    icon.short_description = ''

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('icon', 'first_name', 'last_name')

    def icon(self, obj):
        # Set the primary color to green for the user icon
        return format_html(
            '<i class="fa-duotone fa-user" style="--fa-primary-color: green;"></i>'
        )
    icon.short_description = ''

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('icon', 'product', 'customer', 'date_ordered')

    def icon(self, obj):
        # Set the primary color to orange for the shopping cart icon
        return format_html(
            '<i class="fa-sharp-duotone fa-cart-shopping" style="--fa-primary-color: orange;"></i>'
        )
    icon.short_description = ''
