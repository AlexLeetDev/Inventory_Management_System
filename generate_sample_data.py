import random
from datetime import datetime, timedelta
from inventory.models import Product, Supplier, Customer, Order

# Clear existing data (Optional)
Product.objects.all().delete()
Supplier.objects.all().delete()
Customer.objects.all().delete()
Order.objects.all().delete()

# Generate Suppliers
supplier_names = [
    f"Supplier {i}" for i in range(1, 21)
]  # 20 Suppliers
suppliers = [Supplier.objects.create(name=name) for name in supplier_names]

# Generate Products
product_categories = ["Electronics", "Office Supplies", "Home Appliances", "Accessories"]
product_names = [
    f"{category} Item {i}" for category in product_categories for i in range(1, 26)
]  # 100 Products
products = [
    Product.objects.create(
        name=name,
        price=round(random.uniform(10, 1000), 2)
    )
    for name in product_names
]

# Generate Customers
customer_first_names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Hank"]
customer_last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]
customers = [
    Customer.objects.create(
        first_name=random.choice(customer_first_names),
        last_name=random.choice(customer_last_names)
    )
    for _ in range(200)  # 200 Customers
]

# Generate Orders
for _ in range(1000):  # 1000 Orders
    Order.objects.create(
        product=random.choice(products),
        customer=random.choice(customers),
        date_ordered=datetime.now() - timedelta(days=random.randint(0, 365))  # Random date in the past year
    )

print("Larger dataset successfully generated!")