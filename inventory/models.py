"""
Database models for the Inventory Management System.
Defines suppliers, products, customers, orders, inventory records,
and activity logs used across the application.
"""

from django.db import models

class Supplier(models.Model):
    """Stores supplier information for products."""
    name = models.CharField(max_length=100) 
    contact_email = models.EmailField(blank=True, null=True) 
    phone = models.CharField(max_length=15, blank=True, null=True)  

    def __str__(self):
        return self.name


class Product(models.Model):
    """Represents a product in the inventory system."""
    name = models.CharField(max_length=100) 
    description = models.TextField(blank=True, null=True)  
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    featured = models.BooleanField(default=False)

    class Meta:
        # Custom permissions used for Role-Based Access Control (RBAC)
        permissions = [
            ("can_view_reports", "Can view inventory reports and activity logs"),
            ("can_manage_inventory", "Can add, edit, and delete inventory items"),
        ]

    def __str__(self):
        """Returns the product's name."""
        return self.name


class Customer(models.Model):
    """Represents a customer placing orders."""
    first_name = models.CharField(max_length=50)  
    last_name = models.CharField(max_length=50)  
    email = models.EmailField(blank=True, null=True)  

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Order(models.Model):
    """Represents a customer order for a specific product."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  
    date_ordered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order for {self.product} ({self.quantity}) by {self.customer}"


class Inventory(models.Model):
    """Tracks stock levels for each product."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  
    stock_level = models.PositiveIntegerField()  
    low_stock_threshold = models.PositiveIntegerField(default=10)  

    def __str__(self):
        return f"{self.product.name} - {self.stock_level}"


class ActivityLog(models.Model):
    """Logs system activities for auditing purposes."""
    description = models.TextField()  
    timestamp = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"Activity on {self.timestamp}: {self.description}"