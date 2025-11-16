"""
Management command to set up Role-Based Access Control (RBAC)
for the Inventory Management System.

This command creates three groups:
- Admin
- Manager
- Staff

and assigns the correct permissions to each group based on the
Product model and its custom permissions.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from inventory.models import Product

class Command(BaseCommand):
    help = "Set up RBAC groups and permissions for the Inventory Management System"

    def handle(self, *args, **options):
        self.stdout.write("Setting up RBAC groups and permissions...")

        # Get the content type for the Product model
        product_ct = ContentType.objects.get_for_model(Product)

        # Built-in model permissions for Product
        try:
            add_product = Permission.objects.get(
                codename="add_product",
                content_type=product_ct,
            )
            change_product = Permission.objects.get(
                codename="change_product",
                content_type=product_ct,
            )
            delete_product = Permission.objects.get(
                codename="delete_product",
                content_type=product_ct,
            )
            view_product = Permission.objects.get(
                codename="view_product",
                content_type=product_ct,
            )

            # Custom RBAC permissions defined in Product.Meta
            can_view_reports = Permission.objects.get(
                codename="can_view_reports",
                content_type=product_ct,
            )
            can_manage_inventory = Permission.objects.get(
                codename="can_manage_inventory",
                content_type=product_ct,
            )
        except Permission.DoesNotExist:
            self.stderr.write(
                self.style.ERROR(
                    "One or more permissions do not exist. "
                    "Make sure you have run 'python manage.py makemigrations' "
                    "and 'python manage.py migrate' after adding custom permissions."
                )
            )
            return

        # Create or get groups
        admin_group, _ = Group.objects.get_or_create(name="Admin")
        manager_group, _ = Group.objects.get_or_create(name="Manager")
        staff_group, _ = Group.objects.get_or_create(name="Staff")

        # Admin group: full access to product and inventory-related actions
        admin_permissions = [
            add_product,
            change_product,
            delete_product,
            view_product,
            can_view_reports,
            can_manage_inventory,
        ]
        admin_group.permissions.set(admin_permissions)

        # Manager group: same as Admin for inventory-related features
        manager_permissions = [
            add_product,
            change_product,
            delete_product,
            view_product,
            can_view_reports,
            can_manage_inventory,
        ]
        manager_group.permissions.set(manager_permissions)

        # Staff group: read-only access to products
        staff_permissions = [
            view_product,
        ]
        staff_group.permissions.set(staff_permissions)

        self.stdout.write(self.style.SUCCESS("RBAC groups and permissions configured successfully."))
        self.stdout.write(self.style.SUCCESS("Groups created/updated: Admin, Manager, Staff."))