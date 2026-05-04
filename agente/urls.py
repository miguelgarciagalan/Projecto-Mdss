from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat, name='chat'),
    path('nueva/', views.nueva_conversacion, name='nueva_conversacion'),
    path('mensaje/', views.enviar_mensaje, name='enviar_mensaje'),
]
