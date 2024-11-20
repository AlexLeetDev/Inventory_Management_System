from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=100)  # Supplier name
    contact_email = models.EmailField(blank=True, null=True)  # Optional supplier email
    phone = models.CharField(max_length=15, blank=True, null=True)  # Optional supplier phone number

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)  # Product name
    description = models.TextField(blank=True, null=True)  # Optional product description
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Product price
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)  # Optional supplier link
    featured = models.BooleanField(default=False)  # Field to mark the product as featured

    def __str__(self):
        return self.name


class Customer(models.Model):
    first_name = models.CharField(max_length=50)  # Customer's first name
    last_name = models.CharField(max_length=50)  # Customer's last name
    email = models.EmailField(blank=True, null=True)  # Optional customer email

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Link to Product
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Link to Customer
    quantity = models.PositiveIntegerField(default=1)  # Quantity of products ordered
    date_ordered = models.DateTimeField(auto_now_add=True)  # Order date

    def __str__(self):
        return f"Order for {self.product} ({self.quantity}) by {self.customer}"


class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Link to Product
    stock_level = models.PositiveIntegerField()  # Current stock level
    low_stock_threshold = models.PositiveIntegerField(default=10)  # Low-stock alert threshold

    def __str__(self):
        return f"{self.product.name} - {self.stock_level}"


class ActivityLog(models.Model):
    description = models.TextField()  # Description of activity
    timestamp = models.DateTimeField(auto_now_add=True)  # When the activity occurred

    def __str__(self):
        return f"Activity on {self.timestamp}: {self.description}"