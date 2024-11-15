from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.core import serializers
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

""" Datos de los modelos """
from .models import Product
from .models import ProductImage
from .models import Cart
from .models import CartItem

import json
# Create your views here.

def products_view(request):
    productos = Product.objects.all()

    return render(request, "core/products.html", {"products": productos})


""" Urls relacionadas con el carrito. """

def cart_view(request):
    cart = None
    cartitems = []
    
    if request.user.is_authenticated:    
        cart, created = Cart.objects.get_or_create(customer=request.user, defaults={"status": True})
        cartitems = cart.cartitems.all()

    return render(request, "core/cart.html", {"cart":cart, "cartitems":cartitems})


@login_required
@require_POST  
def add_to_cart(request):
    try:
        data = json.loads(request.body)
        product_id = data.get("id")
        
        if not product_id:
            return JsonResponse({"error": "El ID del producto es obligatorio."}, status=400)

        product = get_object_or_404(Product, id=product_id)

        cart, created = Cart.objects.get_or_create(customer=request.user)
        cart_item, _ = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity += 1
        cart_item.save()

        redirect_url = "/sale/cart"
        return JsonResponse({"redirect": redirect_url}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Formato JSON inválido."}, status=400)

    except Exception as e:
        return JsonResponse({"error": f"Error inesperado: {str(e)}"}, status=500)
    

@login_required
@require_POST  
def delete_from_cart(request):
    try:
        data = json.loads(request.body)
        product_id = data.get("id")

        if not product_id:
            return JsonResponse({"error": "El ID del producto es obligatorio."}, status=400)

        product = get_object_or_404(Product, id=product_id)
        cart, _ = Cart.objects.get_or_create(customer=request.user)
        cart_item = CartItem.objects.filter(cart=cart, product=product).first()

        if cart_item:
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()

            redirect_url = "/sale/cart"
            return JsonResponse({"redirect": redirect_url}, status=200)
        else:
            return JsonResponse({"error": "El producto no está en el carrito."}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Formato JSON inválido."}, status=400)

    except Exception as e:
        # Manejo de errores generales
        return JsonResponse({"error": f"Error inesperado: {str(e)}"}, status=500)

@login_required
@require_POST  
def delete_product_from_cart(request):
    try:
        data = json.loads(request.body)
        product_id = data.get("id")

        if not product_id:
            return JsonResponse({"error": "El ID del producto es obligatorio."}, status=400)

        product = get_object_or_404(Product, id=product_id)
        cart, _ = Cart.objects.get_or_create(customer=request.user)
        cart_item = CartItem.objects.filter(cart=cart, product=product).first()

        if cart_item:
            cart_item.delete()

            redirect_url = "/sale/cart"
            return JsonResponse({"redirect": redirect_url}, status=200)
        else:
            return JsonResponse({"error": "El producto no está en el carrito."}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Formato JSON inválido."}, status=400)

    except Exception as e:
        # Manejo de errores generales
        return JsonResponse({"error": f"Error inesperado: {str(e)}"}, status=500)
