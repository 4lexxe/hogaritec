# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .decorators import redirect_authenticated_user  # Importa el decorador
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from sale.models import Customer
from sale.models import Product

def index(request):
    productos = Product.objects.all()
    
    return render(request, "core/index.html", {"products": productos, 'name': 'index'})  # Usa un diccionario para pasar contexto si es necesario

def acercade_view(request):
    return render(request, "core/acercade.html")

def contacto_view(request):
    return render(request, "core/contacto.html")

# Manejo de errores 404 
def custom_404_view(request, exception):
    return render(request, 'core/404.html', {'path': request.path}, status=404) 

# autenticaciones
@redirect_authenticated_user
def RegisterView(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email').lower()  # Convertir a minúsculas
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        error_en_datos_cliente = False

        # Verificar si el correo electrónico ya existe (con insensibilidad a mayúsculas/minúsculas)
        if Customer.objects.filter(email=email).exists():
            error_en_datos_cliente = True
            messages.error(request, "El correo electrónico ya existe")

        # Verificar la longitud de la contraseña
        if len(password) < 5:
            error_en_datos_cliente = True
            messages.error(request, "La contraseña debe tener al menos 5 caracteres")

        if error_en_datos_cliente:
            return redirect('register')

        try:
            # Crear el nuevo cliente
            nuevo_cliente = Customer.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone,
            )
            nuevo_cliente.set_password(password)
            nuevo_cliente.save()

            messages.success(request, "Cuenta creada. Inicia sesión ahora")
            return redirect('login')
        except IntegrityError:
            # Capturar el error de integridad si el correo ya existe en la base de datos
            messages.error(request, "El correo electrónico ya está registrado. Intenta con otro.")
            return redirect('register')

    return render(request, 'auth/register.html')

@redirect_authenticated_user
def LoginView(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            customer = Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            customer = None

        if customer and customer.check_password(password):
            login(request, customer)
            return redirect('index')
        else:
            messages.error(request, "Credenciales de inicio de sesión incorrectas")
            return redirect('login')

    return render(request, 'auth/login.html')

def LogoutView(request):

    logout(request)

    # redirect to login page after logout
    return redirect('login')