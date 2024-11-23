from django.shortcuts import render
from datetime import datetime
from django.http import JsonResponse
from django.db import transaction
import mercadopago
import os
import json

#Modelos
from sale.models import Cart
from sale.models import CartItem
from sale.models import Order
from sale.models import OrderItem
from sale.models import Payment

def create_order(request):
    cart_id = json.loads(request.body).get("id_cart")
    
    cart = Cart.objects.get(id = cart_id)    
    cartitems = cart.cartitems.all()
    
    try: 
        sdk = mercadopago.SDK(os.getenv('MP_ACCESS_TOKEN'))

        request_options = mercadopago.config.RequestOptions()
        request_options.custom_headers = {
            'x-idempotency-key': '<SOME_UNIQUE_VALUEss>'
        }

        data = {
            "payment_methods": {
                "excluded_payment_methods": [{
                    "installments": 6,
                    "default_installments": 3
                }],
                "excluded_payment_types": [
                    {"id": "ticket"},
                ],
            },
            "items": [
                {
                "id": item.product.id,
                "title": item.product.name,
                "description": "Descripcion del producto",
                "quantity": item.quantity,
                "unit_price": float(item.product.get_final_price()),
                } for item in cartitems
            ],
            
            "back_urls": {
                "success": str(os.getenv("URL_SUCCESS")) + "payment/success",
            },
            "notification_url": "",
            
            "metadata": {
                "id_cart": cart_id,
                "id_customer": cart.customer.id,
            },
        }
        
        preference_response = sdk.preference().create(data)
        preference = preference_response["response"]
        
        return JsonResponse(preference, status=200)
    except Exception as e:
        print("Error: ", e)
        return JsonResponse(preference, status=500)
                

def success(request):
    data = request.GET
        
    sdk = mercadopago.SDK(os.getenv('MP_ACCESS_TOKEN'))
    payment = sdk.payment().get(data["payment_id"])
    response = payment["response"]
        
    cart = Cart.objects.get(id = response["metadata"]["id_cart"])    
    cartitems = cart.cartitems.all()

    try:
        with transaction.atomic():
            # Crear la orden
            order = Order.objects.create(
                customer=cart.customer,
                total_amount = cart.total_price,
                status='pending',
                cart=cart
            )

            # Crear los ítems de la orden
            for cartitem in cartitems:
                OrderItem.objects.create(
                    order=order,
                    product=cartitem.product,
                    quantity=cartitem.quantity,
                    price=cartitem.final_price
                )
            
            # Crear el pagoS
            payment_instance = Payment.objects.create(
                order = order,
                amount = response["transaction_details"]["total_paid_amount"],
                method = response["payment_type_id"],
                status = response["status"],
                transaction_id = response["id"],
                date_approved = response["date_approved"],
                description = response["description"],
                installments = response["installments"],
            )

            # Actualizar el estado de la orden si el pago es exitoso
            if response["status"] == "approved":
                order.status = "completed"
                order.save()

            cartitems.delete()
        
    except Exception as e:
        print(f"Error processing payment: {e}")
    
    return render(request, "core/success.html")

def webhook(request):
    pass


""" 
 "back_urls": {
                "success": "",
                "failure": "",
                "pending": "",
                
            }, 
"""