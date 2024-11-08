from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os

# Create your models here.
""" Modelo para representar un cliente """
class Customer (models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre del cliente")
    surname = models.CharField(max_length=100, verbose_name="Apellido")
    email = models.EmailField(verbose_name="Correo electrónico")
    phone = models.IntegerField(verbose_name="Número de celular")
    avatar = models.ImageField(upload_to="customers/", verbose_name="Avatar", blank=True)
    created = models.DateField(auto_now_add=True, verbose_name="Fecha de registro")
    updated = models.DateField(auto_now=True, verbose_name="Fecha de ultimos cambios de datos")

    def __str__(self):
        return self.name

# Uso de la señal post_delete para eliminar el avatar
@receiver(post_delete, sender=Customer)
def delete_image_product(sender, instance, **kwargs):
    if instance.avatar:
        if os.path.isfile(instance.avatar.path):
            os.remove(instance.avatar.path)

"""Modelo para representar un proveedor."""
class Supplier(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre del proveedor")
    email = models.EmailField(verbose_name="Email")

    def __str__(self):
        return self.name


"""Modelo para representar un producto."""
class Product(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="Código del producto")
    name = models.CharField(max_length=200, verbose_name="Nombre del producto")
    description = models.TextField(verbose_name="Descripción", blank=True)
    brand = models.CharField(max_length=200, verbose_name="Marca del producto", blank=True)
    category = models.CharField(max_length=100, verbose_name="Categoría del producto")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    discount = models.PositiveIntegerField(verbose_name="Descuento", default=0)
    number = models.PositiveIntegerField(verbose_name="Cantidad en inventario")
    
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, verbose_name="Proveedor")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    def __str__(self):
        return f"{self.name} ({self.code})"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="Imágenes", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"Imagen de {self.product.name}"
    
# Uso de la señal post_delete para eliminar la imagen
@receiver(post_delete, sender=ProductImage)
def delete_image_product(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

"""Modelo para representar una venta."""
class Sale(models.Model):
    date = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de la venta")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales', verbose_name="Producto")
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Cliente")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio de venta")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    def __str__(self):
        return f"Venta de {self.product.name} a {self.customer.name if self.customer else 'Cliente desconocido'}"