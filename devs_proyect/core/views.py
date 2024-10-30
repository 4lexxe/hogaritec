# core/views.py
from django.shortcuts import render

def index_view(request):
    return render(request, 'core/index.html')

def acercade_view(request):
    return render(request, 'core/acercade.html')

def contacto_view(request):
    return render(request, 'core/contacto.html')
