# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from sale.models import Customer
from django.contrib.auth.hashers import make_password

def index(request):
    return render(request, "core/index.html", {'name': 'index'})  # Usa un diccionario para pasar contexto si es necesario

def acercade_view(request):
    return render(request, "core/acercade.html")

def contacto_view(request):
    return render(request, "core/contacto.html")

# Manejo de errores 404
def custom_404_view(request, exception):
    return render(request, 'core/404.html', {'path': request.path}, status=404) 

# auth
# Vista de registro
def RegisterView(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        # Validación de errores en los datos del cliente
        error_en_datos_cliente = False

        if Customer.objects.filter(email=email).exists():
            error_en_datos_cliente = True
            messages.error(request, "El correo electrónico ya existe")

        if len(password) < 5:
            error_en_datos_cliente = True
            messages.error(request, "La contraseña debe tener al menos 5 caracteres")

        if error_en_datos_cliente:
            return redirect('register')
        else:
            # Crear un nuevo cliente con los campos correctos
            nuevo_cliente = Customer.objects.create(
                first_name=first_name,  # Usando 'first_name' en lugar de 'name'
                last_name=last_name,    # Usando 'last_name' en lugar de 'surname'
                email=email,
                phone_number=phone,     # Usando 'phone_number' en lugar de 'phone'
            )
            # Establecer la contraseña encriptada
            nuevo_cliente.set_password(password)
            nuevo_cliente.save()

            messages.success(request, "Cuenta creada. Inicia sesión ahora")
            return redirect('login')

    return render(request, 'auth/register.html')

def LoginView(request):
    if request.method == "POST":
        email = request.POST.get("email")  # Cambié 'email' en lugar de 'username'
        password = request.POST.get("password")

        # Buscar al cliente por email
        try:
            customer = Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            customer = None

        # Intentar autenticar al cliente
        if customer and customer.check_password(password):  # Comprobamos la contraseña
            login(request, customer)
            return redirect('index')  # Redirigir a la vista 'index'
        else:
            messages.error(request, "Credenciales de inicio de sesión incorrectas")
            return redirect('login')

    return render(request, 'auth/login.html')
