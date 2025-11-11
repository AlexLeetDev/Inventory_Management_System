from django.views.generic import RedirectView
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from inventory import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Redirect root URL to dashboard
    path('', RedirectView.as_view(pattern_name='dashboard', permanent=False)),

    # Auth
    path('login/',  auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Admin URL
    path('admin/', admin.site.urls),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Product URLs
    path('products/', views.product_list, name='product_list'),  # Product List
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),  # Product Detail
    path('product/add/', views.add_or_edit_product, name='product_add'),  # Add Product
    path('product/edit/<int:product_id>/', views.add_or_edit_product, name='product_edit'),  # Edit Product
    path('toggle_featured/<int:product_id>/', views.toggle_featured, name='toggle_featured'),  # Toggle Featured

    # Inventory Management URLs
    path('add_inventory/<int:product_id>/<int:quantity>/', views.add_inventory, name='add_inventory'),  # Add Inventory
    path('reduce_inventory/<int:product_id>/<int:quantity>/', views.reduce_inventory, name='reduce_inventory'),  # Reduce Inventory

    # Reports and Logs
    path('activity-log/', views.activity_log, name='activity_log'),  # Activity Log
    path('low-stock-report/', views.low_stock_report, name='low_stock_report'),  # Low Stock Report

    # Favicon Redirect
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico')),  # Favicon Redirect
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)