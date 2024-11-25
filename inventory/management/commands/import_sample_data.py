import os
import random
from datetime import datetime, timedelta
from faker import Faker
from django.core.management.base import BaseCommand
from inventory.models import Product, Supplier, Customer, Order, Inventory, ActivityLog

fake = Faker()

class Command(BaseCommand):
    help = "Generate and replace sample data in the database"

    def handle(self, *args, **kwargs):
        # Step 1: Backup existing data
        backup_file = "backup_data.json"
        self.stdout.write("Backing up existing data...")
        os.system(f"python manage.py dumpdata > {backup_file}")
        self.stdout.write(f"Backup completed: {backup_file}")

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
        suppliers = [
            Supplier.objects.create(
                name=fake.company(),
                contact_email=fake.email(),
                phone=fake.phone_number()[:15]
            )
            for _ in range(20)  # 20 Suppliers
        ]

        # Step 4: Generate Products
        self.stdout.write("Creating products...")
        products = [
            Product.objects.create(
                name=fake.word().capitalize(),
                description=fake.sentence(),
                price=round(random.uniform(10, 1000), 2),
                supplier=random.choice(suppliers),
                featured=fake.boolean(chance_of_getting_true=20)
            )
            for _ in range(100)  # 100 Products
        ]

        # Step 5: Generate Customers
        self.stdout.write("Creating customers...")
        customers = [
            Customer.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email()
            )
            for _ in range(200)  # 200 Customers
        ]

        # Step 6: Generate Orders
        self.stdout.write("Creating orders...")
        for _ in range(1000):  # 1000 Orders
            Order.objects.create(
                product=random.choice(products),
                customer=random.choice(customers),
                quantity=random.randint(1, 10),
                date_ordered=datetime.now() - timedelta(days=random.randint(0, 365))
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
        for _ in range(50):  # Log 50 activities
            ActivityLog.objects.create(
                description=fake.sentence(),
                timestamp=datetime.now() - timedelta(days=random.randint(0, 365))
            )

        self.stdout.write("Sample data imported successfully!")
