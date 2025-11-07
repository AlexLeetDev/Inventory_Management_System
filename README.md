# 📦 Inventory_Management_System

An inventory management system with features for product tracking, order processing, and reporting.

## 📊 Current State

The Inventory Management System currently includes:

- ✅ Functional CRUD operations for managing products and suppliers.
- ✅ Automated low-stock alert notifications.
- ⚙️ A basic backend setup using Django.
- 🖥️ A prototype dashboard for interacting with inventory data.

**In Progress**:

- 🚀 Enhancing the dashboard for better user interaction.
- 📈 Adding reporting and analytics features.

## ✨ Features

### ✅ Implemented

- **CRUD Operations**: Add, view, update, and delete products, suppliers, and orders.
- **Low-Stock Alerts**: Notifications are sent when inventory falls below defined thresholds.

### 🛠️ Planned

- **Order Processing**: Track purchase and sales orders, updating inventory levels accordingly.
- **Reporting**: Generate reports on inventory levels, sales trends, and reorder needs.
- **User Authentication**: Implement role-based access control for different user types.

## 🛠️ Tech Stack

- **Backend**: &nbsp; ![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
- **Database**: &nbsp; ![MySQL](https://img.shields.io/badge/MySQL-8.0-blue?logo=mysql&logoColor=white)
- **Frontend**: &nbsp; ![HTML5](https://img.shields.io/badge/HTML5-%23E34F26.svg?logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/CSS3-%231572B6.svg?logo=css3&logoColor=white) ![JavaScript](https://img.shields.io/badge/JavaScript-%23F7DF1E.svg?logo=javascript&logoColor=black)
- **Version Control**: &nbsp; ![Git](https://img.shields.io/badge/Git-F05032?logo=git&logoColor=white) ![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white)

## Project Structure

```plaintext
Inventory_Management_System/
|-- LICENSE                 # License file for the project
|-- README.md               # Project overview and setup instructions
|-- manage.py               # Django management script
|-- requirements.txt        # Python dependencies
|-- inventory/              # Core app for managing products and inventory
|   |-- admin.py            # Admin interface definitions
|   |-- models.py           # Database models for inventory
|   |-- views.py            # View functions for handling requests
|   |-- migrations/         # Database migrations
|   `-- management/         # Custom management commands
|-- inventory_management/   # Project-level configuration
|   |-- settings.py         # Django project settings
|   |-- urls.py             # URL configuration
|   `-- wsgi.py             # WSGI entry point for the project
|-- templates/              # HTML templates for the web application
|   |-- base.html           # Base template for consistent layout
|   |-- admin/              # Custom admin templates
|   |-- inventory/          # Templates for inventory-related views
|   `-- success.html        # Generic success page
|-- static/                 # Static assets (CSS, JavaScript)
|   |-- css/                # Stylesheets
|   `-- js/                 # JavaScript files
|-- source/                 # Documentation source files
|   |-- conf.py             # Sphinx configuration
|   `-- index.rst           # Main documentation file
```

## 🚀 Setup and Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/AlexLeetDev/Inventory_Management_System.git
   cd Inventory_Management_System
   ```

2. Install dependencies:

   ```bash
   python -m venv env
   source env/Scripts/activate
   pip install -r requirements.txt
   ```

3. Set up the environment:
   - Rename `_env.txt` to `.env` and configure the settings as needed.

4. Run the server:

   ```bash
   python manage.py runserver
   ```

5. Access the app at `http://127.0.0.1:8000/`.

## Screenshots

### 1. **Activity Log**

![Activity Log](static/screenshots/activity_log.png)

The activity log provides a history of actions within the system, including inventory updates, user activities, and alerts.

---

### 2. **Customer Management**

![Customer Management](static/screenshots/admin_customer_list.png)

The customer management interface allows admin users to view and modify customer records.

---

### 3. **Admin Dashboard**

![Admin Dashboard](static/screenshots/admin_dashboard.png)

The admin dashboard provides access to various modules, including inventory, customers, and orders.

---

### 4. **Inventory Management**

![Inventory Management](static/screenshots/admin_inventory_list.png)

The inventory management module displays product details and stock levels, with the ability to add or modify inventory records.

---

### 5. **Login Page**

![Login Page](static/screenshots/admin_login.png)

The secure login page ensures that only authorized users can access the system.

---

### 6. **Order Management**

![Order Management](static/screenshots/admin_order_list.png)

The order management module provides an overview of orders, including products, customers, and timestamps.

---

### 7. **Product Management**

![Product Management](static/screenshots/admin_product_list.png)

The product management module allows users to view, add, and edit product details.

---

### 8. **Supplier Management**

![Supplier Management](static/screenshots/admin_supplier_list.png)

The supplier management module lists all suppliers and allows for updates or additions.

---

### 9. **Dashboard Overview**

![Dashboard Overview](static/screenshots/dashboard_overview.png)

The dashboard provides a summary of the inventory, including total stock, low-stock items, and out-of-stock items. It also displays recent activities.

---

### 10. **Highlighting Key Inventory Items**

![Highlight Key Items](static/screenshots/highlight_key_items.png)

The product list highlights key inventory items, such as those with high or low stock levels. Users can toggle the highlight feature on and off for better customization of their view, making it easier to focus on specific products of interest.

---

### 11. **Low Stock Report**

![Low Stock Report](static/screenshots/low_stock_report.png)

The low stock report shows products that have fallen below the threshold, helping users identify items that need to be restocked.

---

### 12. **Product Details**

![Product Details](static/screenshots/product_details.png)

Detailed product information, including price, stock levels, and recent activities, is displayed for individual products.

---

### 13. **Product List**

![Product List](static/screenshots/product_list.png)

The product list shows an overview of all products, their stock levels, and actions available for each product.

---

## Future Enhancements

- Integrate barcode scanning for inventory updates.
- Implement predictive analytics for stock forecasting.
- Add multi-location support for inventory across different warehouses.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
