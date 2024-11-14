from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Supplier, Customer, Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('icon', 'name', 'price', 'stock')

    def icon(self, obj):
        return format_html('<i class="fa-sharp-duotone fa-box" style="--fa-primary-color: #D2691E; --fa-secondary-color: #B8860B;"></i>')
    icon.short_description = ''


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('icon', 'name')

    def icon(self, obj):
        return format_html('<i class="fa-sharp-duotone fa-truck" style="--fa-primary-color: red;"></i>')
    icon.short_description = ''


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('icon', 'first_name', 'last_name')

    def icon(self, obj):
        return format_html('<i class="fa-sharp-duotone fa-user" style="--fa-primary-color: green;"></i>')
    icon.short_description = ''


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('icon', 'product', 'customer', 'date_ordered')

    def icon(self, obj):
        return format_html('<i class="fa-sharp-duotone fa-cart-shopping" style="--fa-primary-color: orange;"></i>')
    icon.short_description = ''
