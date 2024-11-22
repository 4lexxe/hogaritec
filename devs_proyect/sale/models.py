from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_delete
from django.contrib.auth.hashers import make_password
from django.dispatch import receiver
from decimal import Decimal
from django.contrib.auth.models import Permission
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import os

from django.forms.models import model_to_dict

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
    date_joined = models.DateTimeField(default=timezone.now)
    
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

    @property
    def images_urls(self):
        """
        Devuelve una lista de las URLs de todas las imágenes asociadas al producto.
        """
        return [image.image.url for image in self.images.all()]

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

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    date_subscribed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

# Modelos para el carrito de compras -----------------------------------------------------------------

class Cart(models.Model):
    """Modelo para representar un carrito de compras."""
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, verbose_name="Usuario" , related_name="user")
    status = models.BooleanField(default=False, verbose_name="Activo")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    def __str__(self):
        return f"Carrito de {self.customer.first_name}"

    """ Precio final de lo agregado en el carrito """
    @property
    def total_price(self):
        cartitems = self.cartitems.all()
        total = sum([item.final_price for item in cartitems])

        return total
    
    
    """ Cantidad de productos(todos) en el carrito """
    @property
    def num_of_items(self):
        cartitems = self.cartitems.all()
        quantity = sum([item.quantity for item in cartitems])
        return quantity

class CartItem(models.Model):
    """Modelo para representar un elemento en el carrito."""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems', verbose_name="Carrito")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product", verbose_name="Producto")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Cantidad")

    def __str__(self):
        return f"{self.quantity} x {self.product.name} en el carrito"
    
    """ Precio de la cantidad de cada producto aplicado el descuente de cada uno si es que tiene """
    @property
    def final_price(self):
        pricePerProduct = self.product.get_final_price()

        total = pricePerProduct * self.quantity
        return total
    
# Modelos para el registro de las ventas ------------------------------------------------------------------------
"""Modelo para representar una venta."""
class Sale(models.Model):
    
    STATUS_CHOICES = [
        ('paid', 'Pagado'),
        ('pending', 'Pendiente'),
        ('cancelled', 'Cancelado'),
    ]

    id = models.AutoField(primary_key=True, verbose_name="ID de la venta")  # ID único
    date = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de la venta")
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name='sales', verbose_name="Producto"
    )
    customer = models.ForeignKey(
        'Customer', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Cliente"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio de venta")
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="Estado del pedido"
    )
    reference = models.CharField(
        max_length=50, unique=True, verbose_name="Referencia única del pedido", blank=True
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    def save(self, *args, **kwargs):
        """Generar una referencia única antes de guardar."""
        if not self.reference:
            self.reference = f"SALE-{self.id}-{self.date.strftime('%Y%m%d%H%M%S')}"
        super().save(*args, **kwargs)

    def _str_(self):
        customer_name = self.customer.get_full_name() if self.customer else "Cliente desconocido"
        return f"Venta #{self.id} de {self.product.name} a {customer_name} ({self.get_status_display()})"

    class Meta:
        verbose_name = ("Sale")
        verbose_name_plural = ("Sales")
        ordering = ['-date']

#Modelos para el registro de ordenes y pagos

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders', verbose_name="Usuario")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de la venta")
    
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio total de la venta")
    status = models.CharField(max_length=50, choices=(
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ))
    
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Carrito")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Última actualización")
    
    def __str__(self):
        return f"Orden de {self.customer}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitems', verbose_name="Item de orden")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Producto")
    quantity = models.PositiveIntegerField(verbose_name="Cantidad")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    
    def __str__(self):
        return f"Item de {self.order}"

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto") 
    method = models.CharField(max_length=50, verbose_name="Metodo de pago")  
    status = models.CharField(max_length=50, verbose_name="Estado")
    transaction_id = models.CharField(max_length=255, null=True, blank=True, verbose_name="Id de transaccion")
    date_approved = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de aprobacion del pago")
    description = models.TextField(null=True, blank=True, verbose_name="Descripcion")
    installments = models.PositiveIntegerField(default=1, verbose_name="Cuotas")  

    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creacion")  
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualizacion") 

    def __str__(self):
        return f"Payment {self.id} - Order {self.order.id} - {self.status}"