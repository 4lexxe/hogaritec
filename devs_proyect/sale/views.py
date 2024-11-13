from django.shortcuts import render, redirect


""" Datos de los modelos """
from .models import Product
from .models import ProductImage

# Create your views here.

def products_view(request):
    productos = Product.objects.all()

    return render(request, "core/products.html", {"products": productos})