from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Categoria, Cliente, Produto
from .forms import CategoriaForm, ClienteForm, ProdutoForm

def index(request):
    return render(request, 'index.html')

# --- CATEGORIAS ---

def categoria(request):
    contexto = {
        'lista': Categoria.objects.all().order_by('-id'),
    }
    return render(request, 'categoria/lista.html', contexto)

def form_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria salva com sucesso!')
            return redirect('categoria')
        else:
            messages.error(request, 'Erro ao salvar a categoria.')
    else:
        form = CategoriaForm()
    return render(request, 'categoria/form.html', {'form': form})

def editar_categoria(request, id):
    categoria_obj = get_object_or_404(Categoria, pk=id)
    if request.method == 'POST':    
        form = CategoriaForm(request.POST, instance=categoria_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria atualizada!')
            return redirect('categoria')
    else:    
        form = CategoriaForm(instance=categoria_obj)
    return render(request, 'categoria/form.html', {'form': form})

def remover_categoria(request, id):
    categoria_obj = get_object_or_404(Categoria, pk=id)
    categoria_obj.delete()
    messages.success(request, 'Categoria removida com sucesso!')
    return redirect('categoria')

# --- CLIENTES ---

def cliente(request):
    contexto = {'lista': Cliente.objects.all().order_by('-id')}
    return render(request, 'cliente/lista.html', contexto)

def form_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente salvo com sucesso!')
            return redirect('cliente')
    else:
        form = ClienteForm()
    return render(request, 'cliente/form.html', {'form': form})

def editar_cliente(request, id):
    cliente_obj = get_object_or_404(Cliente, pk=id)
    if request.method == 'POST':    
        form = ClienteForm(request.POST, instance=cliente_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente atualizado!')
            return redirect('cliente')
    else:    
        form = ClienteForm(instance=cliente_obj)
    return render(request, 'cliente/form.html', {'form': form})

def remover_cliente(request, id):
    cliente_obj = get_object_or_404(Cliente, pk=id)
    cliente_obj.delete()
    messages.success(request, 'Cliente removido!')
    return redirect('cliente')

# --- PRODUTOS ---

def produto(request):
    contexto = {'lista': Produto.objects.all().order_by('-id')}
    return render(request, 'produto/lista.html', contexto)