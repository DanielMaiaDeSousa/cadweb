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


def remover_categoria(request, id):
    categoria_obj = get_object_or_404(Categoria, pk=id)
    categoria_obj.delete()
    messages.success(request, 'Categoria removida com sucesso!')
    return redirect('categoria')

def detalhes_categoria(request, id):
    categoria = get_object_or_404(Categoria, pk=id)
    return render(request, 'categoria/detalhes.html', {'item': categoria})

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

def form_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto salvo com sucesso!')
            return redirect('produto')
    else:
        form = ProdutoForm()
    return render(request, 'produto/form.html', {'form': form})

def editar_produto(request, id):
    # Busca o produto pelo ID ou retorna 404 se não existir
    produto_obj = get_object_or_404(Produto, pk=id)
    
    if request.method == 'POST':
        # Passa os dados do POST e a instância do produto existente para o formulário
        form = ProdutoForm(request.POST, instance=produto_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto atualizado com sucesso!')
            return redirect('produto')
    else:
        # Carrega o formulário preenchido com os dados atuais do produto
        form = ProdutoForm(instance=produto_obj)
    
    return render(request, 'produto/form.html', {'form': form})

def remover_produto(request, id):
    produto_obj = get_object_or_404(Produto, pk=id)
    produto_obj.delete()
    messages.success(request, 'Produto removido com sucesso!')
    return redirect('produto')