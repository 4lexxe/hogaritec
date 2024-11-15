from django.urls import path
from . import views


urlpatterns = [
    path('products/', views.products_view, name='productos'),
    path('cart/', views.cart_view, name="cart"),
    path("add_to_cart", views.add_to_cart, name= "añadir"),
    path("delete_from_cart", views.delete_from_cart, name="eliminar"),
    path("delete_product_from_cart", views.delete_product_from_cart, name="eliminarProductoDelCarrito")
]  