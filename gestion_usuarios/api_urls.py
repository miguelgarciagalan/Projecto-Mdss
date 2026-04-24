from django.urls import path

from gestion_usuarios.api_views import ProductorViewSet

productor_list = ProductorViewSet.as_view({'get': 'list', 'post': 'create'})
productor_detail = ProductorViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'})

urlpatterns = [
    path('productores/', productor_list, name='api-productores-list'),
    path('productores/<int:pk>/', productor_detail, name='api-productores-detail'),
]
