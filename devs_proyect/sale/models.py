from django.db import models


# Create your models here.
class Customer (models.Model):
    """ Modelo para representar un cliente """
    name = models.CharField(max_length=200, verbose_name="Nombre del cliente")
    surname = models.CharField(max_length=100, verbose_name="Apellido")
    email = models.EmailField(verbose_name="Correo electrónico")
    phone = models.IntegerField(verbose_name="Número de celular")
    avatar = models.ImageField(upload_to="customers/", verbose_name="Avatar", blank=True)
    created = models.DateField(auto_now_add=True, verbose_name="Fecha de registro")
    updated = models.DateField(auto_now=True, verbose_name="Fecha de ultimos cambios de datos")

    def __str__(self):
        return self.name

    
class Supplier(models.Model):
    """Modelo para representar un proveedor."""
    name = models.CharField(max_length=200, verbose_name="Nombre del proveedor")
    email = models.EmailField(verbose_name="Email")

    def __str__(self):
        return self.name

class Product(models.Model):
    """Modelo para representar un producto."""
    code = models.CharField(max_length=50, unique=True, verbose_name="Código del producto")
    name = models.CharField(max_length=200, verbose_name="Nombre del producto")
    description = models.TextField(verbose_name="Descripción", blank=True)
    category = models.CharField(max_length=100, verbose_name="Categoría del producto")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    discount = models.PositiveIntegerField(verbose_name="Descuento", default=0)
    number = models.PositiveIntegerField(verbose_name="Cantidad en inventario")
    images = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Imágenes")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, verbose_name="Proveedor")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    def __str__(self):
        return f"{self.name} ({self.code})"



class Sale(models.Model):
    """Modelo para representar una venta."""
    date = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de la venta")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales', verbose_name="Producto")
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Cliente")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio de venta")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    def __str__(self):
        return f"Venta de {self.product.name} a {self.customer.name if self.customer else 'Cliente desconocido'}"
