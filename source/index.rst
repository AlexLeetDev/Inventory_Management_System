.. Inventory Management System documentation master file, created by
   sphinx-quickstart on Sat Nov 23 01:03:24 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Inventory Management System documentation
=========================================

Add your content using ``reStructuredText`` syntax. See the
`reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_
documentation for details.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   introduction
   installation
   usage
   models
   views
   admin

Introduction
============

The **Inventory Management System (IMS)** is a project designed to showcase skills in backend development, database modeling, and web application design using Django. It is a simplified inventory tracking system for managing products, suppliers, customers, and orders. This project highlights best practices in:

- Implementing **CRUD operations**.
- Using **Django models** to define a database schema.
- Customizing the Django **admin interface**.
- Enhancing **frontend templates** for better user experience.
- Generating **reports** to showcase data analytics.

As a personal project, the IMS is not intended for production use but serves as an example of technical abilities and problem-solving skills.

---

## Key Features

- **Product Management**: Add, view, update, and delete inventory items.
- **Order Tracking**: Create and manage orders, linking products and customers.
- **Low-Stock Alerts**: Identify products that need restocking.
- **Report Generation**: Export inventory and order data in PDF or Excel formats.
- **Customizable Frontend Templates**: Tailored HTML templates for a clean, intuitive user interface.
- **Customizable Admin Panel**: Enhanced Django admin interface for easy management.

---

Installation
============

1. **Clone the Repository**:
   Clone the Inventory Management System project from GitHub:
   ```bash
   git clone https://github.com/AlexLeetDev/Inventory_Management_System.git
   ```

2. **Navigate to the Project Directory**:
   Move into the project's directory:
   ```bash
   cd Inventory_Management_System
   ```

3. **Set Up a Virtual Environment**:
   Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install Dependencies**:
   Install all required dependencies using `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set Up the Database**:
   Run database migrations to initialize the database schema:
   ```bash
   python manage.py migrate
   ```

6. **Create a Superuser (Optional)**:
   If you want to access the Django admin panel, create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server**:
   Start the Django development server:
   ```bash
   python manage.py runserver
   ```

8. **Access the Application**:
   Open your browser and navigate to:
   ```
   http://127.0.0.1:8000/
   ```

   To access the admin interface, go to:
   ```
   http://127.0.0.1:8000/admin/
   ```

For more information and updates, visit the project repository on GitHub: [Inventory Management System](https://github.com/AlexLeetDev/Inventory_Management_System)

---

Usage
=====

### Product Management
- Add new products via the "Add Product" page.
- View a list of products and edit or delete them as needed.

### Order Management
- Create new orders, linking products and customers.
- Track order details and update their status.

### Reporting
- Generate inventory or sales reports in PDF or Excel formats.

---

Models
======

This section documents the database models used in the Inventory Management System.

.. automodule:: inventory.models
   :members:
   :undoc-members:
   :show-inheritance:

---

Views
=====

This section provides an overview of the views used in the application.

.. automodule:: inventory.views
   :members:
   :undoc-members:

---

Admin
=====

Details of the customizations made to the Django admin interface.

.. automodule:: inventory.admin
   :members:
   :undoc-members:

---

Templates
=========

This section highlights the customizations made to the frontend templates of the Inventory Management System. These templates are designed to provide a user-friendly interface, emphasizing simplicity and functionality.

### Key Templates

1. **Base Template (`base.html`)**:
   - Serves as the foundation for all other templates.
   - Includes a consistent header, navigation bar, and footer.
   - Dynamically loads the content of each page using `{% block content %}`.
   - Incorporates FontAwesome icons and custom CSS for enhanced visuals.

   **Notable Features**:
   - Centralized navigation links for:
     - Dashboard
     - Products
     - Activity Log
     - Low Stock Report
   - Responsive design using CSS (`styles.css`) for consistent rendering on different devices.

2. **Dashboard (`dashboard.html`)**:
   - Displays key metrics like total stock, low-stock items, and out-of-stock items.
   - Includes dynamically updating progress bars for stock levels.
   - Features a recent activities section to summarize recent system actions.

   **Highlight**:
   - Uses embedded JavaScript to calculate and visualize stock data with progress bars.

3. **Add or Edit Product (`add_or_edit_product.html`)**:
   - Provides a form for adding or editing products in the inventory.
   - Dynamically adjusts the title and icons based on whether the user is adding or editing a product.

   **Features**:
   - Inline error handling to display validation errors.
   - CSRF token for secure form submissions.

4. **Product List (`product_list.html`)**:
   - Lists all products in a table, including stock levels and featured status.
   - Includes pagination controls for navigating through long lists.

   **Interactive Feature**:
   - JavaScript for toggling a product’s "featured" status dynamically via AJAX.

5. **Low Stock Report (`low_stock_report.html`)**:
   - Displays a table of products with stock levels below a specified threshold.
   - Helps users quickly identify items that need restocking.

6. **Activity Log (`activity_log.html`)**:
   - Shows a paginated list of recent activities in the system, such as product updates or order placements.
   - Includes pagination controls for easy navigation.

7. **Success and Error Templates (`success.html`, `error.html`)**:
   - Provides feedback to the user after completing an action.
   - **Success**: Displays a success message and a link back to the dashboard.
   - **Error**: Shows an error message and a "Go Back" button.

8. **Product Detail (`product_detail.html`)**:
   - Displays detailed information about a specific product, including price, stock level, and recent activity.

   **Low Stock Alert**:
   - Highlights products with critically low stock levels using a warning message.

---

### Custom CSS and JavaScript

1. **CSS (`styles.css`)**:
   - Implements a consistent color scheme and layout.
   - Enhances usability with clean, modern styles for buttons, tables, and forms.

2. **JavaScript**:
   - Adds interactivity, such as progress bar updates and AJAX-powered toggling of featured status.

---

### Code Snippet: Dashboard Template

Here’s an example snippet from the dashboard template:

```html
<div class="dashboard-container">
    <div class="metric-box">
        <h3 class="dashboard-number">{{ total_stock|default:0 }}</h3>
        <p><i class="fa-light fa-box"></i> Total Stock</p>
        <div class="progress-bar">
            <div class="progress" id="total-stock-progress"></div>
        </div>
    </div>
</div>
```

This snippet dynamically displays stock metrics and visual progress bars, giving users an at-a-glance overview of inventory health.

---


