# devs_proyect/urls.py
from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('', views.index_view, name='index'),  # Ruta para la página de inicio
    path('admin/', admin.site.urls),
    path('acercade/', views.acercade_view, name='about'),  # Ruta para la página "Acerca de"
    path('contacto/', views.contacto_view, name='contacto'),
]
