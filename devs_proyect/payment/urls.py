from django.urls import path
from . import views


urlpatterns = [
    #Urls relacionadas con los pagos
    path("create_order", views.create_order, name="create_order"),
    path("success", views.success),
    path("webhook", views.webhook),
]  