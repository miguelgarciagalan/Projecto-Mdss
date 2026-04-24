from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_produccion, name='lista_produccion'),
    path('<int:produccion_id>/', views.detalle_produccion, name='detalle_produccion'),
]