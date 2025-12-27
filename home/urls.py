from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('categoria/', views.categoria, name="categoria"),
    path('categoria/form', views.form_categoria, name="form_categoria"),
]