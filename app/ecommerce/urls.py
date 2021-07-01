from django.urls import path

from app.ecommerce import views
from app.ecommerce.views import *

app_name = 'ecommerce'

urlpatterns = [
    # home
    path('', DashboardView.as_view(), name='dashboard'),
    path('contacto/', ContactoView.as_view(), name='contacto'),
    path('acerca/', AcercaView.as_view(), name='about'),
    # categorias
    path('categoria/list/', CategoriaListView.as_view(), name='categoria_list'),
    path('categoria/add/', CategoriaCreateView.as_view(), name='categoria_create'),
    path('categoria/update/<int:pk>/', CategoriaUpdateView.as_view(), name='categoria_update'),
    path('categoria/delete/<int:pk>/', CategoriaDeleteView.as_view(), name='categoria_delete'),
    path('categoria/productos/<int:pk>/', ProductosCategoriaListView.as_view(), name='producto_categoria_list'),
    # productos
    path('producto/list/', ProductoListView.as_view(), name='producto_list'),
    path('producto/add/', ProductoCreateView.as_view(), name='producto_create'),
    path('producto/update/<int:pk>/', ProductoUpdateView.as_view(), name='producto_update'),
    path('producto/delete/<int:pk>/', ProductoDeleteView.as_view(), name='producto_delete'),
    # productos Vista Usuario
    path('productos/list/', ProductoUsuarioListView.as_view(), name='producto_usuario_list'),
    path('productos/view/<int:pk>/', ProductoView.as_view(), name='producto_view'),
    path('view/<int:pk>/', ProductoDashboardView.as_view(), name='dashboard_view'),
    # carrito
    path('carrito/add/', views.addCart, name='carrito_add'),
    path('carrito/list/', CarritoListView.as_view(), name='carrito_list'),
    path('carrito/delete/<int:pk>/', CarritoDeleteView.as_view(), name='carrito_delete'),
    path('carrito/purchase/', views.purchaseCart, name='carrito_purchase'),
]