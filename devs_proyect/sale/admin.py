from django.contrib import admin

from .models import Customer
from .models import Supplier
from .models import Product
from .models import Sale
from .models import ProductImage

# Register your models here.

class ImagenProductoInline(admin.TabularInline):
    model = ProductImage
    extra = 3  # Número de imágenes adicionales en blanco que se mostrarán

class ProductoAdmin(admin.ModelAdmin):
    inlines = [ImagenProductoInline]

admin.site.register(Product, ProductoAdmin)
admin.site.register(Customer)
admin.site.register(Supplier)
admin.site.register(Sale)