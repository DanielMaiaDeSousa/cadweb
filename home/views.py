from django.shortcuts import render, redirect
from django.db import connection, DatabaseError
from .models import *
from .forms import *
from .forms import CategoriaForm  # Adicione esta linha se não existir

def index(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')  # Teste de conexão
    except DatabaseError as e:
        return render(request, 'index.html', {'error': 'Erro de conexão com o banco de dados: ' + str(e)})

    return render(request, 'index.html')

def categoria(request):
    contexto = {
        'lista': Categoria.objects.all().order_by('-id'),
    }
    return render(request, 'categoria/lista.html',contexto)

def form_categoria(request):
    if request.method == 'POST':
       form = CategoriaForm(request.POST) # instancia o modelo com os dados do form
       if form.is_valid():# faz a validação do formulário
            form.save() # salva a instancia do modelo no banco de dados
            return redirect('categoria') # redireciona para a listagem
    else:# método é get, novo registro
        form = CategoriaForm() # formulário vazio
    contexto = {
        'form':form,
    }
    return render(request, 'categoria/formulario.html', contexto)
