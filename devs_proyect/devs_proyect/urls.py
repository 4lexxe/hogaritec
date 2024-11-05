# devs_proyect/urls.py
from django.contrib import admin
from django.urls import path
from core import views
from django.conf.urls import handler404
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),  # Ruta para la página de inicio
    path('admin/', admin.site.urls),
    path('acercade/', views.acercade_view, name='about'),  # Ruta para la página "Acerca de"
    path('contacto/', views.contacto_view, name='contacto'),  # Ruta para la página "Contacto"
]

# Asigna la función personalizada a handler404
handler404 = 'core.views.custom_404_view'


if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)