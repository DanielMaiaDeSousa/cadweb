from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    
    # --- CATEGORIAS ---
    path('categoria/', views.categoria, name="categoria"),
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
    path('cliente/form/', views.form_cliente, name="form_cliente"),
    path('cliente/editar/<int:id>/', views.editar_cliente, name="editar_cliente"),
    path('cliente/remover/<int:id>/', views.remover_cliente, name='remover_cliente'),
    path('cliente/detalhes/<int:id>/', views.detalhes_cliente, name='detalhes_cliente'),
    
    path('buscar_dados/<str:app_model>/', views.buscar_dados, name='buscar_dados'),
    path('produto/estoque/<int:id>/', views.ajustar_estoque, name='ajustar_estoque'),
    
    # --- PEDIDOS ---
    path('pedido/', views.pedido, name='pedido'),
    path('novo_pedido/<int:cliente_id>/', views.novo_pedido, name='novo_pedido'),
    path('detalhes_pedido/<int:id>/', views.detalhes_pedido, name='detalhes_pedido'),
    path('pedido/remover-item/<int:id>/', views.remover_item_pedido, name='remover_item_pedido'),
    path('pedido/remover/<int:id>/', views.remover_pedido, name='remover_pedido'),
    
    # --- PAGAMENTOS ---
    path('pedido/pagamento/<int:pedido_id>/', views.registrar_pagamento, name='registrar_pagamento'),
    path('pagamento/<int:pagamento_id>/editar/', views.editar_pagamento, name='editar_pagamento'),
    path('pagamento/<int:pagamento_id>/remover/', views.remover_pagamento, name='remover_pagamento'),
    
    # home/urls.py
    path('pedido/<int:pedido_id>/nota_fiscal/', views.nota_fiscal, name='nota_fiscal'),
]