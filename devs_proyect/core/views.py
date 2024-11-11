from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .decorators import redirect_authenticated_user
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from .models import PasswordReset
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
import uuid
from django.http import HttpResponse

from sale.models import Customer
from sale.models import Product

Customer = get_user_model()

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

def ForgotPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email').lower()

        try:
            user = Customer.objects.get(email=email)
            
            # Verificar si el usuario tiene un token válido que aún no ha expirado
            existing_token = PasswordReset.objects.filter(user=user, expires_at__gt=timezone.now()).first()

            if existing_token:
                # Si ya hay un token válido, redirige al usuario al enlace para restablecer la contraseña
                messages.info(request, 'Ya se ha enviado un enlace de restablecimiento a este correo recientemente.')
                return redirect('password-reset-sent', token=existing_token.token)

            # Si no hay token válido, se crea uno nuevo (incluso si el anterior ha expirado)
            password_reset = PasswordReset.objects.create(user=user, email=email)
            
            # Generar la URL para el restablecimiento de contraseña
            reset_url = request.build_absolute_uri(reverse('reset-password', kwargs={'token': password_reset.token}))

            # Construir el cuerpo del correo
            email_body = f'Restablece la contraseña de tu cuenta de Hogaritec usando el siguiente link:\n\n{reset_url}'
            
            # Enviar el correo
            email_message = EmailMessage(
                subject='Restablece tu contraseña',
                body=email_body,
                from_email=settings.EMAIL_HOST_USER,
                to=[email]
            )
            email_message.send(fail_silently=True)

            # Redirigir al usuario a una página de confirmación con el nuevo token
            return render(request, 'auth/password_reset_sent.html', {'email': email})

        except Customer.DoesNotExist:
            # Mensaje genérico para evitar indicar que el correo no existe
            messages.info(request, 'Si el correo es válido, se ha enviado un enlace de restablecimiento.')
            return redirect('password-reset-sent-generic')  # Página genérica sin `token`

    return render(request, 'auth/forgot_password.html')

def PasswordResetSentGeneric(request):
    # Renderizar una página genérica para el mensaje de restablecimiento de contraseña
    return render(request, 'auth/password_reset_sent_generic.html')

def PasswordResetSent(request, token):
    # Verificar si el token existe en la base de datos
    try:
        password_reset = PasswordReset.objects.get(token=token)
        return render(request, 'auth/password_reset_sent.html')
    except PasswordReset.DoesNotExist:
        return render(request, 'invalid_token.html')
    
def ResetPassword(request, token):
    try:
        # Busca el registro de restablecimiento usando el token
        password_reset = PasswordReset.objects.get(token=token)
    except PasswordReset.DoesNotExist:
        messages.error(request, 'Enlace de restablecimiento inválido')
        return redirect('forgot-password')

    # Verifica si el enlace ha expirado
    expiration_time = password_reset.created_at + timezone.timedelta(minutes=10)
    if timezone.now() > expiration_time:
        password_reset.delete()  # Elimina el registro del enlace expirado
        messages.error(request, 'El enlace de restablecimiento ha expirado')
        return redirect('forgot-password')

    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Verifica que las contraseñas no sean None y que coincidan
        if not password or not confirm_password:
            messages.error(request, 'Por favor, ingresa ambas contraseñas')
        elif password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden')
        elif len(password) < 5:
            messages.error(request, 'La contraseña debe tener al menos 5 caracteres')
        else:
            # Establece la nueva contraseña
            user = password_reset.user
            user.set_password(password)
            user.save()
            password_reset.delete()  # Borra el registro de restablecimiento
            messages.success(request, 'Contraseña restablecida correctamente. Ahora puedes iniciar sesión.')
            return redirect('login')

    return render(request, 'auth/reset_password.html', {'token': token})