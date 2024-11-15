from django.contrib import admin
from .models import Customer
from .models import Supplier
from .models import Product
from .models import Sale
from .models import ProductImage
from django.contrib import admin
from .models import Customer, Supplier, Product, Sale, ProductImage, Cart, CartItem
from .models import Subscriber

# Registrar el modelo Customer con una administración personalizada
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name', 'phone_number', 'avatar')}),
        ('Permisos', {'fields': ('is_staff', 'is_superuser', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'first_name', 'last_name', 'phone_number', 'is_staff', 'is_superuser'),
        }),
    )

# Configuración de ProductImage para ser inluso dentro del formulario de edición de Producto
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Número de imágenes que se mostrarán por defecto

# Administración personalizada para el modelo Product
class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'price', 'category', 'supplier', 'number')
    search_fields = ('name', 'category', 'supplier__name')
    inlines = [ProductImageInline]  # Agregar las imágenes dentro de la edición de productos

# Registrar los modelos en el panel de administración
admin.site.register(Product, ProductAdmin)
admin.site.register(Supplier)
admin.site.register(Sale)
admin.site.register(Customer, CustomerAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'created', 'updated')  # Agrega 'id' a la lista de campos a mostrar

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)

#admin para las suscripciones al newsletter
@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_subscribed')
    search_fields = ('email',)
    list_filter = ('date_subscribed',)