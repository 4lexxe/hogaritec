from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_delete
from django.contrib.auth.hashers import make_password
from django.dispatch import receiver
from django.db import models
from decimal import Decimal
from django.contrib.auth.models import Permission
import os

class CustomerManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Crea y guarda un usuario con un correo electrónico y una contraseña.
        """
        if not email:
            raise ValueError("El correo electrónico debe ser proporcionado")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Crea y guarda un superusuario.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class Customer(AbstractBaseUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    
    # Los campos de autenticación estándar de Django
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Establecemos el gestor de usuarios
    objects = CustomerManager()

    # Usamos el email como nombre de usuario
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone_number"]

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super().save(*args, **kwargs)

    # Implementing required permissions methods
    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

# Usage of post_delete signal for deleting avatar
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

    # Fucion para calcular el descuento
    def get_final_price(self):
        discount_decimal = Decimal(self.discount) / Decimal('100')
        final_price = self.price * (1 - discount_decimal)
        
        # Redondear a dos decimales
        return final_price.quantize(Decimal('0.01'))


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
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