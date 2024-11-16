import logging
from django.shortcuts import render
from .models import Product, Inventory, ActivityLog
from django.db.models import Sum

# Create a logger instance
logger = logging.getLogger('django')


def dashboard(request):
    try:
        # Calculate total stock across all products
        total_stock = Inventory.objects.aggregate(total_stock=Sum('stock_level'))['total_stock'] or 0

        # Count low-stock and out-of-stock products
        low_stock_items = Inventory.objects.filter(stock_level__lt=10).count()
        out_of_stock_items = Inventory.objects.filter(stock_level=0).count()

        # Fetch recent activity logs
        recent_activities = ActivityLog.objects.order_by('-timestamp')[:10]

        logger.info("Dashboard data retrieved successfully.")

        # Pass data to the template
        context = {
            'total_stock': total_stock,
            'low_stock_items': low_stock_items,
            'out_of_stock_items': out_of_stock_items,
            'recent_activities': recent_activities,
        }
        return render(request, 'dashboard.html', context)
    except Exception as e:
        logger.error(f"Error while loading dashboard: {e}")
        return render(request, 'error.html', {'message': "An error occurred while loading the dashboard."})


def product_list(request):
    try:
        # Display a list of all products with their stock levels
        products_with_stock = Inventory.objects.select_related('product').all()
        logger.info("Product list retrieved successfully.")

        context = {
            'products_with_stock': products_with_stock,
        }
        return render(request, 'product_list.html', context)
    except Exception as e:
        logger.error(f"Error while loading product list: {e}")
        return render(request, 'error.html', {'message': "An error occurred while loading the product list."})


def add_inventory(request, product_id, quantity):
    try:
        # Add stock to an existing product in the inventory
        product = Product.objects.get(id=product_id)
        inventory, created = Inventory.objects.get_or_create(product=product)
        inventory.stock_level += quantity
        inventory.save()

        # Log the activity
        ActivityLog.objects.create(description=f"Added {quantity} to {product.name}'s stock.")
        logger.info(f"Added {quantity} units to {product.name}.")

        return render(request, 'success.html', {'message': f"Successfully added {quantity} units to {product.name}."})
    except Exception as e:
        logger.error(f"Error while adding inventory for product {product_id}: {e}")
        return render(request, 'error.html', {'message': "An error occurred while adding inventory."})


def reduce_inventory(request, product_id, quantity):
    try:
        # Reduce stock for a product in the inventory
        product = Product.objects.get(id=product_id)
        inventory = Inventory.objects.get(product=product)
        
        if inventory.stock_level < quantity:
            logger.warning(f"Not enough stock to reduce {quantity} units from {product.name}.")
            return render(request, 'error.html', {'message': "Not enough stock to reduce."})

        inventory.stock_level -= quantity
        inventory.save()

        # Log the activity
        ActivityLog.objects.create(description=f"Reduced {quantity} from {product.name}'s stock.")
        logger.info(f"Reduced {quantity} units from {product.name}.")

        return render(request, 'success.html', {'message': f"Successfully reduced {quantity} units from {product.name}."})
    except Exception as e:
        logger.error(f"Error while reducing inventory for product {product_id}: {e}")
        return render(request, 'error.html', {'message': "An error occurred while reducing inventory."})