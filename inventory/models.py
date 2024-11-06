from django.db import models

# Create your models here.

from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)  # Product name
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Product price
    stock = models.PositiveIntegerField()  # Number of items in stock

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=100)  # Supplier name

    def __str__(self):
        return self.name

class Customer(models.Model):
    first_name = models.CharField(max_length=50)  # Customer's first name
    last_name = models.CharField(max_length=50)  # Customer's last name

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Link to Product
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Link to Customer
    date_ordered = models.DateTimeField(auto_now_add=True)  # Order date

    def __str__(self):
        return f"Order for {self.product} by {self.customer}"

