from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection, DatabaseError
from .models import *
from .forms import *
from .forms import CategoriaForm  # Adicione esta linha se não existir
from django.contrib import messages

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

def editar_categoria(request, id):
    categoria = Categoria.objects.get(pk=id)
    if request.method == 'POST':
        # combina os dados do formulário submetido com a instância do objeto existente, permitindo editar seus valores.
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            categoria = form.save() # save retorna o objeto salvo
            return redirect('categoria') # redireciona para a listagem
    else:
         form = CategoriaForm(instance=categoria)
    return render(request, 'categoria/formulario.html', {'form': form,})

def detalhes_categoria(request, id):
    # Busca a categoria ou retorna erro 404 se não existir
    categoria = get_object_or_404(Categoria, pk=id)
    return render(request, 'categoria/detalhes.html', {'item': categoria})

def remover_categoria(request, id):
    try:
        categoria = Categoria.objects.get(pk=id)
        categoria.delete()
        messages.success(request, 'Categoria removida com sucesso!')
    except Categoria.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
    
    return redirect('categoria')