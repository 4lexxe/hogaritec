from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages

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
def add_to_cart(request):
    data = json.loads(request.body)
    product_id = data["id"]
    product = Product.objects.get(id=product_id)
    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(customer=request.user)


        cartitem, created =CartItem.objects.get_or_create(cart=cart, product=product)
        
        cartitem.quantity += 1
        cartitem.save()
    
    
    return JsonResponse({"redirect": "/sale/cart"}, safe=False)

@login_required
def delete_to_the_cart(request):
    data = json.loads(request.body)
    product_id = data["id"]
    product = Product.objects.get(id=product_id)
    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(customer=request.user)


        cartitem, created =CartItem.objects.get_or_create(cart=cart, product=product)
        
        # Disminuye en uno si la cantidad es mayor a 0
        if cartitem.quantity > 0:
            cartitem.quantity -= 1
            cartitem.save()

        # Elimina en el caso que la cantidad del producto sea 0
        if not cartitem.quantity:
            cartitem.delete()
    
    
    return JsonResponse({"redirect": "/sale/cart"}, safe=False)

#Para despues
def confirm_payment(request, pk):
    cart = Cart.objects.get(id=pk)
    cart.completed = True
    cart.save()
    messages.success(request, "Payment made successfully")
    return redirect("index")
