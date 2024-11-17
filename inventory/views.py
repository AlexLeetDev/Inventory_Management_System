import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import JsonResponse
from django.conf import settings
from .models import Product, Inventory, ActivityLog
from .forms import ProductForm

# Create a logger instance
logger = logging.getLogger('django')

def dashboard(request):
    try:
        # Calculate total stock across all products
        total_stock = Inventory.objects.aggregate(total_stock=Sum('stock_level'))['total_stock'] or 0

        # Count low-stock and out-of-stock products
        low_stock_items = Inventory.objects.filter(stock_level__lt=settings.LOW_STOCK_THRESHOLD).count()
        out_of_stock_items = Inventory.objects.filter(stock_level=0).count()

        # Fetch recent activity logs
        recent_activities = ActivityLog.objects.order_by('-timestamp')[:10]

        logger.info("Dashboard data retrieved successfully.")

        context = {
            'total_stock': total_stock,
            'low_stock_items': low_stock_items,
            'out_of_stock_items': out_of_stock_items,
            'recent_activities': recent_activities,
        }
        return render(request, 'inventory/dashboard.html', context)
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
        return render(request, 'inventory/product_list.html', context)
    except Exception as e:
        logger.error(f"Error while loading product list: {e}")
        return render(request, 'error.html', {'message': "An error occurred while loading the product list."})


def product_detail(request, product_id):
    try:
        # Fetch product details and inventory
        product = get_object_or_404(Product, id=product_id)
        inventory = Inventory.objects.get(product=product)
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


def activity_log(request):
    try:
        # Paginate activity logs
        activities = ActivityLog.objects.order_by('-timestamp')
        paginator = Paginator(activities, 20)  # 20 logs per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
        }
        return render(request, 'inventory/activity_log.html', context)
    except Exception as e:
        logger.error(f"Error while loading activity log: {e}")
        return render(request, 'error.html', {'message': "An error occurred while loading the activity log."})


def add_or_edit_product(request, product_id=None):
    try:
        product = None
        if product_id:
            product = get_object_or_404(Product, id=product_id)

        if request.method == "POST":
            form = ProductForm(request.POST, instance=product)
            if form.is_valid():
                form.save()
                message = "Product updated successfully." if product else "Product added successfully."
                logger.info(message)
                return render(request, 'success.html', {'message': message})
        else:
            form = ProductForm(instance=product)

        context = {
            'form': form,
            'product': product,
        }
        return render(request, 'inventory/add_or_edit_product.html', context)
    except Exception as e:
        logger.error(f"Error while adding/editing product: {e}")
        return render(request, 'error.html', {'message': "An error occurred while saving the product."})


def low_stock_report(request):
    try:
        # Get threshold from query params or use default
        threshold = int(request.GET.get('threshold', settings.LOW_STOCK_THRESHOLD))
        low_stock_products = Inventory.objects.filter(stock_level__lt=threshold).select_related('product')

        context = {
            'low_stock_products': low_stock_products,
            'threshold': threshold,
        }
        return render(request, 'inventory/low_stock_report.html', context)
    except Exception as e:
        logger.error(f"Error while generating low stock report: {e}")
        return render(request, 'error.html', {'message': "An error occurred while generating the low stock report."})


def add_inventory(request, product_id, quantity):
    try:
        # Get the product and inventory
        product = get_object_or_404(Product, id=product_id)
        inventory, created = Inventory.objects.get_or_create(product=product)

        # Update stock level
        inventory.stock_level += quantity
        inventory.save()

        # Log the activity
        logger.info(f"Added {quantity} units to {product.name}.")
        return JsonResponse({'message': f"Successfully added {quantity} units to {product.name}."})
    except Exception as e:
        logger.error(f"Error adding inventory: {e}")
        return JsonResponse({'error': str(e)}, status=400)


def reduce_inventory(request, product_id, quantity):
    try:
        # Get the product and inventory
        product = get_object_or_404(Product, id=product_id)
        inventory = Inventory.objects.get(product=product)

        # Check if stock is sufficient to reduce
        if inventory.stock_level < quantity:
            logger.warning(f"Not enough stock to reduce {quantity} units from {product.name}.")
            return JsonResponse({'error': "Not enough stock to reduce."}, status=400)

        # Reduce stock level
        inventory.stock_level -= quantity
        inventory.save()

        # Log the activity
        logger.info(f"Reduced {quantity} units from {product.name}.")
        return JsonResponse({'message': f"Successfully reduced {quantity} units from {product.name}."})
    except Exception as e:
        logger.error(f"Error reducing inventory: {e}")
        return JsonResponse({'error': str(e)}, status=400)