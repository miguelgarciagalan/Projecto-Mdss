from django.urls import path
from . import views

urlpatterns = [
    path('lotes/', views.lista_lotes, name='lista_lotes'),
    path('lotes/<int:lote_id>/', views.detalle_lote, name='detalle_lote'),
]