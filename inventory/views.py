"""
Views for the Inventory Management System.

RBAC rules:
- All main pages require login.
- Users with "can_manage_inventory" may add/edit/delete products or change stock.
- Users with "can_view_reports" may access reports and activity logs.
"""

import logging
import re

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required

from .models import Product, Inventory, ActivityLog
from .forms import ProductForm

logger = logging.getLogger('django')


@permission_required("inventory.can_manage_inventory", raise_exception=True)
def toggle_featured(request, product_id):
    """
    Toggle a product's featured status.

    RBAC:
    - Only users with "can_manage_inventory" can modify a product.
    """
    if request.method == 'POST':
        try:
            product = Product.objects.get(id=product_id)
            product.featured = not product.featured
            product.save()
            return JsonResponse({'message': 'Product status updated!', 'featured': product.featured})
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found.'}, status=404)


@login_required
def dashboard(request):
    """
    Show a summary of stock levels and recent activity.

    RBAC:
    - Any logged-in user may view the dashboard.
    """
    try:
        total_stock = Inventory.objects.aggregate(total_stock=Sum('stock_level'))['total_stock'] or 0
        low_stock_items = Inventory.objects.filter(stock_level__lt=settings.LOW_STOCK_THRESHOLD).count()
        out_of_stock_items = Inventory.objects.filter(stock_level=0).count()
        recent_activities = ActivityLog.objects.order_by('-timestamp')[:10]
        max_capacity = getattr(settings, 'MAX_CAPACITY', 10000)

        context = {
            'total_stock': total_stock,
            'low_stock_items': low_stock_items,
            'out_of_stock_items': out_of_stock_items,
            'max_capacity': max_capacity,
            'recent_activities': recent_activities,
        }
        return render(request, 'inventory/dashboard.html', context)
    except Exception as e:
        logger.error(f"Error while loading dashboard: {e}")
        return render(request, 'error.html', {'message': "An error occurred while loading the dashboard."})


def sort_key(obj):
    """
    Helper to sort products by name.
    If the name ends in a number, sort by the text part first,
    then by the number. Otherwise, sort by name and put it at the end.
    """
    match = re.search(r'(\D*)(\d+)$', obj.product.name)
    if match:
        main_text = match.group(1)
        number = int(match.group(2))
        return (main_text.strip().lower(), number)
    else:
        return (obj.product.name.lower(), float('inf'))


@login_required
def product_list(request):
    """
    Show all products with their stock levels.

    RBAC:
    - Any logged-in user can view the product list.
    """
    try:
        products_with_stock = Inventory.objects.select_related('product')
        sorted_products = sorted(products_with_stock, key=sort_key)

        paginator = Paginator(sorted_products, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'inventory/product_list.html', {'page_obj': page_obj})
    except Exception as e:
        logger.error(f"Error while loading product list: {e}")
        return render(request, 'error.html', {'message': "An error occurred while loading the product list."})


@login_required
def product_detail(request, product_id):
    """
    Show details, stock information, and recent activity for one product.

    RBAC:
    - Any logged-in user can view product details.
    """
    try:
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


@permission_required("inventory.can_view_reports", raise_exception=True)
def activity_log(request):
    """
    Show a paginated list of system activity.

    RBAC:
    - Only users with "can_view_reports" can view the activity log.
    """
    try:
        activities = ActivityLog.objects.order_by('-timestamp')
        paginator = Paginator(activities, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'inventory/activity_log.html', {'page_obj': page_obj})
    except Exception as e:
        logger.error(f"Error while loading activity log: {e}")
        return render(request, 'error.html', {'message': "An error occurred while loading the activity log."})


@permission_required("inventory.can_manage_inventory", raise_exception=True)
def add_or_edit_product(request, product_id=None):
    """
    Add a new product or edit an existing one.

    RBAC:
    - Only users with "can_manage_inventory" can add or edit products.
    """
    try:
        product = None
        if product_id:
            product = get_object_or_404(Product, id=product_id)

        if request.method == "POST":

            form = ProductForm(request.POST, instance=product)
            if form.is_valid():
                form.save()
                message = "Product updated successfully." if product else "Product added successfully."
                return render(request, 'success.html', {'message': message})
        else:
            form = ProductForm(instance=product)

        return render(request, 'inventory/add_or_edit_product.html', {'form': form, 'product': product})
    except Exception as e:
        logger.error(f"Error while adding/editing product: {e}")
        return render(request, 'error.html', {'message': "An error occurred while saving the product."})


@permission_required("inventory.can_view_reports", raise_exception=True)
def low_stock_report(request):
    """
    Show a report of products below a stock threshold.

    RBAC:
    - Only users with "can_view_reports" can view this report.
    """
    try:
        threshold = int(request.GET.get('threshold', settings.LOW_STOCK_THRESHOLD))
        low_stock_products = Inventory.objects.filter(stock_level__lt=threshold).select_related('product')

        context = {'low_stock_products': low_stock_products, 'threshold': threshold,}
        return render(request, 'inventory/low_stock_report.html', context)
    except Exception as e:
        logger.error(f"Error while generating low stock report: {e}")
        return render(request, 'error.html', {'message': "An error occurred while generating the low stock report."})


@permission_required("inventory.can_manage_inventory", raise_exception=True)
def add_inventory(request, product_id, quantity):
    """
    Increase the stock level for a product.

    RBAC:
    - Only users with "can_manage_inventory" can change stock levels.
    """
    try:
        product = get_object_or_404(Product, id=product_id)
        inventory, _ = Inventory.objects.get_or_create(product=product)

        inventory.stock_level += quantity
        inventory.save()

        return JsonResponse({'message': f"Successfully added {quantity} units to {product.name}."})
    except Exception as e:
        logger.error(f"Error adding inventory: {e}")
        return JsonResponse({'error': str(e)}, status=400)


@permission_required("inventory.can_manage_inventory", raise_exception=True)
def reduce_inventory(request, product_id, quantity):
    """
    Decrease the stock level for a product.

    RBAC:
    - Only users with "can_manage_inventory" can change stock levels.
    """
    try:
        product = get_object_or_404(Product, id=product_id)
        inventory = Inventory.objects.get(product=product)

        if inventory.stock_level < quantity:
            return JsonResponse({'error': "Not enough stock to reduce."}, status=400)

        inventory.stock_level -= quantity
        inventory.save()

        return JsonResponse({'message': f"Successfully reduced {quantity} units from {product.name}."})
    except Exception as e:
        logger.error(f"Error reducing inventory: {e}")
        return JsonResponse({'error': str(e)}, status=400)
