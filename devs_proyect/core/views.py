from django.shortcuts import HttpResponse,render


# Create your views here.
def index(request):
    return render(request,"core/index.html")

def acercade_view(request):
    return render(request, "core/acercade.html")