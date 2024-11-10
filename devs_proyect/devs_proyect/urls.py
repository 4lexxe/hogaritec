# devs_proyect/urls.py
from django.contrib import admin
from django.urls import path, include
from core import views
from django.conf import settings
from django.conf.urls import handler404
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views


# app_name = 'core'  # Esta línea no es necesaria aquí, ya que el archivo 'urls.py' de 'core' maneja las rutas específicas de la app core

urlpatterns = [
    # Ruta para la página de inicio (esta ruta ya es parte de 'core.urls', no necesitas incluir devs_proyect.urls aquí)
    path('', views.index, name='index'),
    
    # Rutas de administración
    path('admin/', admin.site.urls),
    
    # Otras rutas relacionadas con la aplicación 'core'
    path('acercade/', views.acercade_view, name='about'),
    path('contacto/', views.contacto_view, name='contacto'),
    
    # Incluyendo las rutas de la app 'sale'
    path('sale/', include('sale.urls')),

    # Rutas de autenticación
    path('register/', views.RegisterView, name='register'),
    path('login/', views.LoginView, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

# Asigna la función personalizada a handler404
handler404 = 'core.views.custom_404_view'

# Si estás en modo DEBUG, servir los archivos estáticos y de medios
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
