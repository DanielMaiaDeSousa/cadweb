from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('categoria/', views.categoria, name="categoria"),
    path('cliente/', views.cliente, name="cliente"),
    path('produto/', views.produto, name="produto"),    path('salvar_categoria/', views.salvar_categoria, name="salvar_categoria"),
    path('salvar_cliente/', views.salvar_cliente, name="salvar_cliente"),
    path('salvar_produto/', views.salvar_produto, name="salvar_produto"),
    path('editar_categoria/<int:id>/', views.editar_categoria, name="editar_categoria"),
    path('editar_cliente/<int:id>/', views.editar_cliente, name="editar_cliente"),
    path('editar_produto/<int:id>/', views.editar_produto, name="editar_produto"),
    path('atualizar_categoria/<int:id>/', views.atualizar_categoria, name="atualizar_categoria"),
    path('atualizar_cliente/<int:id>/', views.atualizar_cliente, name="atualizar_cliente"),
    path('atualizar_produto/<int:id>/', views.atualizar_produto, name="atualizar_produto"),
    path('deletar_categoria/<int:id>/', views.deletar_categoria, name="deletar_categoria"),
    path('deletar_cliente/<int:id>/', views.deletar_cliente, name="deletar_cliente"),
    path('deletar_produto/<int:id>/', views.deletar_produto, name="deletar_produto"),   
]