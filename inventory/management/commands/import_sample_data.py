import os
import random
from datetime import datetime, timedelta
from faker import Faker
from django.core.management.base import BaseCommand
from inventory.models import Product, Supplier, Customer, Order, Inventory, ActivityLog

fake = Faker()

class Command(BaseCommand):
    help = "Generate and replace realistic sample data in the database"

    def add_arguments(self, parser):
        parser.add_argument('--skip-backup', action='store_true', help='Skip backing up existing data')

    def handle(self, *args, **kwargs):
        # Step 1: Backup existing data (if not skipped)
        if not kwargs['skip_backup']:
            backup_file = "backup_data.json"
            self.stdout.write("Backing up existing data...")
            os.system(f"python manage.py dumpdata > {backup_file}")
            self.stdout.write(f"Backup completed: {backup_file}")
        else:
            self.stdout.write("Skipping backup as requested...")

        # Step 2: Clear existing data
        self.stdout.write("Clearing existing data...")
        Order.objects.all().delete()
        Inventory.objects.all().delete()
        Product.objects.all().delete()
        Supplier.objects.all().delete()
        Customer.objects.all().delete()
        ActivityLog.objects.all().delete()

        # Step 3: Generate Suppliers
        self.stdout.write("Creating suppliers...")
        supplier_names = [
            "TechPro", "HomeEase", "GadgetCo", "ElectroHub", "FutureTech",
        ]
        suppliers = [
            Supplier.objects.create(
                name=name,
                contact_email=f"{name.lower()}@example.com",
                phone=fake.phone_number()[:15]
            )
            for name in supplier_names
        ]

        # Step 4: Generate Products
        self.stdout.write("Creating electronic products...")
        categories = {
            "Electronics": [
                "Smartphone", "Laptop", "Tablet", "Headphones", "Smartwatch",
                "Gaming Console", "Monitor", "Router", "Bluetooth Speaker",
                "Keyboard", "Mouse", "Camera", "Drone", "Power Bank"
            ]
        }
        price_ranges = {
            "Smartphone": (500, 1500),
            "Laptop": (800, 2500),
            "Tablet": (300, 800),
            "Headphones": (50, 300),
            "Smartwatch": (150, 500),
            "Gaming Console": (400, 800),
            "Monitor": (200, 600),
            "Router": (50, 300),
            "Bluetooth Speaker": (30, 200),
            "Keyboard": (20, 100),
            "Mouse": (10, 80),
            "Camera": (300, 1200),
            "Drone": (500, 2000),
            "Power Bank": (20, 100),
        }
        concise_descriptions = {
            "Smartphone": "A fast and stylish smartphone.",
            "Laptop": "A powerful laptop for work and play.",
            "Tablet": "A portable tablet with great performance.",
            "Headphones": "High-quality noise-cancelling headphones.",
            "Smartwatch": "A smartwatch with health tracking features.",
            "Gaming Console": "A console for immersive gaming.",
            "Monitor": "A monitor with vibrant display quality.",
            "Router": "A router with reliable connectivity.",
            "Bluetooth Speaker": "A compact and portable speaker.",
            "Keyboard": "A durable keyboard with smooth keys.",
            "Mouse": "An ergonomic mouse for precision.",
            "Camera": "A camera for capturing clear images.",
            "Drone": "A drone with easy controls and great footage.",
            "Power Bank": "A lightweight power bank for charging devices.",
        }
        products = []
        for product_name in categories["Electronics"]:
            price_range = price_ranges[product_name]
            description = concise_descriptions.get(product_name, f"A high-quality {product_name.lower()}.")

            for _ in range(3):  # Create 3 variations for each product
                products.append(
                    Product.objects.create(
                        name=f"{random.choice(['Deluxe', 'Pro', 'Ultra', 'Mini', 'Max'])} {product_name} {fake.random_number(digits=3, fix_len=True)}",
                        description=description,  # Assign concise description here
                        price=round(random.uniform(*price_range), 2),
                        supplier=random.choice(suppliers),
                        featured=random.choice([True, False]),
                    )
                )

        # Step 5: Generate Customers
        self.stdout.write("Creating customers...")
        customers = [
            Customer.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email()
            )
            for _ in range(100)  # 100 Customers
        ]

        # Step 6: Generate Orders
        self.stdout.write("Creating orders...")
        for _ in range(200):  # 200 Orders
            Order.objects.create(
                product=random.choice(products),
                customer=random.choice(customers),
                quantity=random.randint(1, 10),
                date_ordered=datetime.now() - timedelta(days=random.randint(0, 30))
            )

        # Step 7: Generate Inventory
        self.stdout.write("Creating inventory...")
        for product in products:
            Inventory.objects.create(
                product=product,
                stock_level=random.randint(10, 200),
                low_stock_threshold=random.randint(5, 20)
            )

        # Step 8: Generate Activity Logs
        self.stdout.write("Creating activity logs...")
        activity_messages = [
            "New product added to inventory.",
            "Order placed by a customer.",
            "Stock level updated for a product.",
            "Supplier details modified.",
            "Customer information updated.",
            "Low-stock alert issued for a product.",
            "Order shipment completed.",
            "Inventory threshold reached.",
            "Admin user logged in.",
            "Activity log cleared."
        ]
        for _ in range(50):  # Log 50 activities
            ActivityLog.objects.create(
                description=random.choice(activity_messages),
                timestamp=datetime.now() - timedelta(days=random.randint(0, 30))
            )

        self.stdout.write("Sample data imported successfully!")
