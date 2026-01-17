from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    
    # --- CATEGORIAS ---
    path('categoria/', views.categoria, name="categoria"),
    # ADICIONE ESTA LINHA:
    path('categoria/form/', views.form_categoria, name="form_categoria"), 
    path('categoria/editar/<int:id>/', views.editar_categoria, name="editar_categoria"),
    path('categoria/detalhes/<int:id>/', views.detalhes_categoria, name='detalhes_categoria'),
    path('categoria/remover/<int:id>/', views.remover_categoria, name='remover_categoria'),
    
    # --- PRODUTOS ---
    path('produto/', views.produto, name="produto"),
    path('produto/form/', views.form_produto, name="form_produto"),
    path('produto/editar/<int:id>/', views.editar_produto, name="editar_produto"),
    path('produto/remover/<int:id>/', views.remover_produto, name='remover_produto'),
    path('produto/detalhes/<int:id>/', views.detalhes_produto, name='detalhes_produto'),
    
    # --- CLIENTES --- 
    path('cliente/', views.cliente, name="cliente"),   
    # ADICIONE ESTA LINHA:
    path('cliente/form/', views.form_cliente, name="form_cliente"),
    path('cliente/editar/<int:id>/', views.editar_cliente, name="editar_cliente"),
    path('cliente/remover/<int:id>/', views.remover_cliente, name='remover_cliente'),
    path('cliente/detalhes/<int:id>/', views.detalhes_cliente, name='detalhes_cliente'),
]