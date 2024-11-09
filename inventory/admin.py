from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Supplier, Customer, Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('icon', 'name', 'price', 'stock')

    def icon(self, obj):
        return format_html('<i class="fas fa-box"></i>')
    icon.short_description = 'Icon'

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('icon', 'name')

    def icon(self, obj):
        return format_html('<i class="fas fa-truck"></i>')
    icon.short_description = 'Icon'

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('icon', 'first_name', 'last_name')

    def icon(self, obj):
        return format_html('<i class="fas fa-user"></i>')
    icon.short_description = 'Icon'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('icon', 'product', 'customer', 'date_ordered')

    def icon(self, obj):
        return format_html('<i class="fas fa-shopping-cart"></i>')
    icon.short_description = 'Icon'
