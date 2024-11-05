from django.contrib import admin

from .models import Customer
from .models import Supplier
from .models import Product
from .models import Sale

# Register your models here.

admin.site.register(Customer)
admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(Sale)