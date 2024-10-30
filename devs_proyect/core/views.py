# core/views.py
from django.shortcuts import render

def index(request):
    return render(request, "core/index.html", {'name': 'index'})  # Usa un diccionario para pasar contexto si es necesario

def acercade_view(request):
    return render(request, "core/acercade.html")

def contacto_view(request):
    return render(request, "core/contacto.html")

# Manejo de errores 404
def custom_404_view(request, exception):
    return render(request, 'core/404.html', {'path': request.path}, status=404)
