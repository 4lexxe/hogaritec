from django.contrib import messages
from django.shortcuts import redirect

def redirect_authenticated_user(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "Ya has iniciado sesión.")
            return redirect('index')  # Redirige a 'index' o la vista que prefieras
        return view_func(request, *args, **kwargs)
    return wrapper
