from django.urls import path
from . import views
from .views import delete_product_image

urlpatterns = [
    # Dashboard Views
    path('dashboard/', views.dashboard_view, name='dashboard'),  # Vista principal del dashboard
    path('products/', views.products_dashboard_view, name='products_dashboard_view'),  # Vista de productos en el dashboard
    path('subscribers/', views.subscribers_dashboard_view, name='subscribers_dashboard_view'),  # Vista de suscriptores en el dashboard
    path('sales/', views.sales_dashboard_view, name='sales_dashboard_view'),  # Vista de ventas en el dashboard
    path('customers/', views.customers_dashboard_view, name='customers_dashboard_view'),  # Vista de clientes en el dashboard
    path('suppliers/', views.suppliers_dashboard_view, name='suppliers_dashboard_view'),  # Vista de proveedores en el dashboard

    # Product Management URLs
    path('add-product/', views.add_product, name='add_product'),  # Agregar producto
    path('edit-product/', views.edit_product, name='edit_product'),  # Editar producto
    path('delete-product/', views.delete_product, name='delete_product'),  # Eliminar producto
    path('delete-product-image/', views.delete_product_image, name='delete_product_image'),  # Eliminar imagen de producto (es redundante, por lo que se elimina una de las rutas duplicadas)

    # Subscriber Management URLs
    path('add-subscriber/', views.add_subscriber, name='add_subscriber'),  # Agregar suscriptor
    path('edit-subscriber/', views.edit_subscriber, name='edit_subscriber'),  # Editar suscriptor
    path('delete-subscriber/', views.delete_subscriber, name='delete_subscriber'),  # Eliminar suscriptor

    # Supplier Management URLs
    path('add_supplier/', views.add_supplier, name='add_supplier'),  # Agregar proveedor
    path('edit_supplier/<int:supplier_id>/', views.edit_supplier, name='edit_supplier'),  # Editar proveedor por ID
    path('delete_supplier/<int:supplier_id>/', views.delete_supplier, name='delete_supplier'),  # Eliminar proveedor por ID

    # Sale Management URLs
    path('delete_sale/', views.delete_sale, name='delete_sale'),  # Eliminar venta

    # Customer Management URLs
    path('customers/add/', views.add_customer, name='add_customer'),  # Agregar cliente
    path('customers/edit/', views.edit_customer, name='edit_customer'),  # Editar cliente
    path('customers/delete/', views.delete_customer, name='delete_customer'),  # Eliminar cliente
]
