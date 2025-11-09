import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import JsonResponse
from django.conf import settings
from .models import Product, Inventory, ActivityLog
from .forms import ProductForm
import re

# Create a logger to record messages for debugging and tracking
logger = logging.getLogger('django')

# -----------------------------
# Toggle the "featured" status of a product
# -----------------------------
def toggle_featured(request, product_id):
    if request.method == 'POST':  # Make sure it's a POST request
        try:
            # Find the product by its ID
            product = Product.objects.get(id=product_id)
            # Change the featured status (True -> False, or False -> True)
            product.featured = not product.featured
            product.save()  # Save the change to the database
            return JsonResponse({'message': 'Product status updated!', 'featured': product.featured})
        except Product.DoesNotExist:
            # If the product ID doesn’t exist, return an error message
            return JsonResponse({'error': 'Product not found.'}, status=404)

# -----------------------------
# Dashboard view to show summary info
# -----------------------------
def dashboard(request):
    try:
        # Add up the total stock from all products
        total_stock = Inventory.objects.aggregate(total_stock=Sum('stock_level'))['total_stock'] or 0

        # Count how many products are low on stock
        low_stock_items = Inventory.objects.filter(stock_level__lt=settings.LOW_STOCK_THRESHOLD).count()

        # Count how many products are completely out of stock
        out_of_stock_items = Inventory.objects.filter(stock_level=0).count()

        # Get the 10 most recent activity log entries
        recent_activities = ActivityLog.objects.order_by('-timestamp')[:10]

        # Use a default capacity limit if none is set in settings
        max_capacity = getattr(settings, 'MAX_CAPACITY', 10000)

        # Record success in the log
        logger.info("Dashboard data retrieved successfully.")

        # Send data to the dashboard template
        context = {
            'total_stock': total_stock,
            'low_stock_items': low_stock_items,
            'out_of_stock_items': out_of_stock_items,
            'max_capacity': max_capacity,
            'recent_activities': recent_activities,
        }
        return render(request, 'inventory/dashboard.html', context)
    except Exception as e:
        # Log any error that happens and show an error page
        logger.error(f"Error while loading dashboard: {e}")
        return render(request, 'error.html', {'message': "An error occurred while loading the dashboard."})

# -----------------------------
# Helper function for sorting products with numbers in their names
# -----------------------------
def sort_key(obj):
    # Try to find a number at the end of the product name
    match = re.search(r'(\D*)(\d+)$', obj.product.name)
    if match:
        # Separate the name into text and number parts
        main_text = match.group(1)
        number = int(match.group(2))
        # Sort alphabetically by name first, then numerically by number
        return (main_text.strip().lower(), number)
    else:
        # If no number found, just sort by name and send to the end
        return (obj.product.name.lower(), float('inf'))

# -----------------------------
# Product list page
# -----------------------------
def product_list(request):
    try:
        # Get all products and their inventory info
        products_with_stock = Inventory.objects.select_related('product')

        # Sort products using the helper function
        sorted_products = sorted(products_with_stock, key=sort_key)

        # Set up pagination (10 products per page)
        paginator = Paginator(sorted_products, 10)
        page_number = request.GET.get('page')  # Get the current page number
        page_obj = paginator.get_page(page_number)  # Get that page’s items

        logger.info("Product list retrieved successfully with pagination.")

        context = {
            'page_obj': page_obj,
        }
        return render(request, 'inventory/product_list.html', context)
    except Exception as e:
        logger.error(f"Error while loading product list: {e}")
        return render(request, 'error.html', {'message': "An error occurred while loading the product list."})

# -----------------------------
# Product detail page
# -----------------------------
def product_detail(request, product_id):
    try:
        # Get the product or show 404 if not found
        product = get_object_or_404(Product, id=product_id)
        # Get inventory record for this product
        inventory = Inventory.objects.get(product=product)
        # Show recent activity related to this product
        activities = ActivityLog.objects.filter(description__icontains=product.name).order_by('-timestamp')[:10]

        context = {
            'product': product,
            'inventory': inventory,
            'activities': activities,
        }
        return render(request, 'inventory/product_detail.html', context)
    except Exception as e:
        logger.error(f"Error while loading product details for product {product_id}: {e}")
        return render(request, 'error.html', {'message': "An error occurred while loading product details."})

# -----------------------------
# Activity log page
# -----------------------------
def activity_log(request):
    try:
        # Get all activities sorted by most recent first
        activities = ActivityLog.objects.order_by('-timestamp')
        # Show 20 per page
        paginator = Paginator(activities, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
        }
        return render(request, 'inventory/activity_log.html', context)
    except Exception as e:
        logger.error(f"Error while loading activity log: {e}")
        return render(request, 'error.html', {'message': "An error occurred while loading the activity log."})

# -----------------------------
# Add or edit a product
# -----------------------------
def add_or_edit_product(request, product_id=None):
    try:
        product = None
        if product_id:
            # Get product if editing an existing one
            product = get_object_or_404(Product, id=product_id)

        if request.method == "POST":
            # Fill the form with submitted data
            form = ProductForm(request.POST, instance=product)
            if form.is_valid():
                # Save new or edited product
                form.save()
                message = "Product updated successfully." if product else "Product added successfully."
                logger.info(message)
                return render(request, 'success.html', {'message': message})
        else:
            # If not a POST request, show an empty form or product info
            form = ProductForm(instance=product)

        context = {
            'form': form,
            'product': product,
        }
        return render(request, 'inventory/add_or_edit_product.html', context)
    except Exception as e:
        logger.error(f"Error while adding/editing product: {e}")
        return render(request, 'error.html', {'message': "An error occurred while saving the product."})

# -----------------------------
# Low stock report page
# -----------------------------
def low_stock_report(request):
    try:
        # Use threshold from URL if given, otherwise use default
        threshold = int(request.GET.get('threshold', settings.LOW_STOCK_THRESHOLD))
        # Get products below the threshold
        low_stock_products = Inventory.objects.filter(stock_level__lt=threshold).select_related('product')

        context = {
            'low_stock_products': low_stock_products,
            'threshold': threshold,
        }
        return render(request, 'inventory/low_stock_report.html', context)
    except Exception as e:
        logger.error(f"Error while generating low stock report: {e}")
        return render(request, 'error.html', {'message': "An error occurred while generating the low stock report."})

# -----------------------------
# Add inventory (increase stock)
# -----------------------------
def add_inventory(request, product_id, quantity):
    try:
        # Get the product and its inventory
        product = get_object_or_404(Product, id=product_id)
        inventory, created = Inventory.objects.get_or_create(product=product)

        # Increase stock level
        inventory.stock_level += quantity
        inventory.save()

        # Record the action in logs
        logger.info(f"Added {quantity} units to {product.name}.")
        return JsonResponse({'message': f"Successfully added {quantity} units to {product.name}."})
    except Exception as e:
        logger.error(f"Error adding inventory: {e}")
        return JsonResponse({'error': str(e)}, status=400)

# -----------------------------
# Reduce inventory (decrease stock)
# -----------------------------
def reduce_inventory(request, product_id, quantity):
    try:
        # Get the product and its inventory
        product = get_object_or_404(Product, id=product_id)
        inventory = Inventory.objects.get(product=product)

        # Check if enough stock is available
        if inventory.stock_level < quantity:
            logger.warning(f"Not enough stock to reduce {quantity} units from {product.name}.")
            return JsonResponse({'error': "Not enough stock to reduce."}, status=400)

        # Subtract the given quantity
        inventory.stock_level -= quantity
        inventory.save()

        # Record the action in logs
        logger.info(f"Reduced {quantity} units from {product.name}.")
        return JsonResponse({'message': f"Successfully reduced {quantity} units from {product.name}."})
    except Exception as e:
        logger.error(f"Error reducing inventory: {e}")
        return JsonResponse({'error': str(e)}, status=400)
