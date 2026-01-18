from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.apps import apps

# Importação de todos os modelos (Atividades 14 e 16)
from .models import Categoria, Cliente, Produto, Estoque, Pedido, ItemPedido

# Importação de todos os formulários (Lembre-se de mover o ItemPedidoForm para o forms.py)
from .forms import CategoriaForm, ClienteForm, ProdutoForm, EstoqueForm, ItemPedidoForm

# --- INDEX ---
def index(request):
    return render(request, 'index.html')

# --- CATEGORIAS ---
def categoria(request):
    contexto = {'lista': Categoria.objects.all().order_by('ordem')}
    return render(request, 'categoria/lista.html', contexto)

def form_categoria(request):
    form = CategoriaForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria salva com sucesso!')
            return redirect('categoria')
    return render(request, 'categoria/formulario.html', {'form': form})

def editar_categoria(request, id):
    categoria_obj = get_object_or_404(Categoria, pk=id)
    form = CategoriaForm(request.POST or None, instance=categoria_obj)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria atualizada!')
            return redirect('categoria')
    return render(request, 'categoria/formulario.html', {'form': form})

def detalhes_categoria(request, id):
    item = get_object_or_404(Categoria, pk=id)
    return render(request, 'categoria/detalhes.html', {'item': item})

def remover_categoria(request, id):
    item = get_object_or_404(Categoria, pk=id)
    item.delete()
    messages.success(request, 'Categoria removida!')
    return redirect('categoria')

# --- CLIENTES ---
def cliente(request):
    contexto = {'lista': Cliente.objects.all().order_by('-id')}
    return render(request, 'cliente/lista.html', contexto)

def form_cliente(request):
    form = ClienteForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente cadastrado com sucesso!')
            return redirect('cliente')
    return render(request, 'cliente/form.html', {'form': form})

def editar_cliente(request, id):
    cliente_obj = get_object_or_404(Cliente, pk=id)
    form = ClienteForm(request.POST or None, instance=cliente_obj)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados do cliente atualizados!')
            return redirect('cliente')
    return render(request, 'cliente/form.html', {'form': form})

def detalhes_cliente(request, id):
    item = get_object_or_404(Cliente, pk=id)
    return render(request, 'cliente/detalhes.html', {'item': item})

def remover_cliente(request, id):
    item = get_object_or_404(Cliente, pk=id)
    item.delete()
    messages.success(request, 'Cliente removido!')
    return redirect('cliente')

# --- PRODUTOS ---
def produto(request):
    contexto = {'lista': Produto.objects.all().order_by('-id')}
    return render(request, 'produto/lista.html', contexto)

def form_produto(request):
    form = ProdutoForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto salvo com sucesso!')
            return redirect('produto')
    return render(request, 'produto/form.html', {'form': form})

def editar_produto(request, id):
    produto_obj = get_object_or_404(Produto, pk=id)
    form = ProdutoForm(request.POST or None, instance=produto_obj)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto atualizado!')
            return redirect('produto')
    return render(request, 'produto/form.html', {'form': form})

def detalhes_produto(request, id):
    produto = get_object_or_404(Produto, pk=id)
    return render(request, 'produto/detalhes.html', {'item': produto})

def remover_produto(request, id):
    item = get_object_or_404(Produto, pk=id)
    item.delete()
    messages.success(request, 'Produto removido!')
    return redirect('produto')

# --- ESTOQUE (Atividade 14) ---
def ajustar_estoque(request, id):
    produto = get_object_or_404(Produto, pk=id)
    estoque, created = Estoque.objects.get_or_create(produto=produto)
    
    if request.method == 'POST':
        form = EstoqueForm(request.POST, instance=estoque)
        if form.is_valid():
            form.save()
            messages.success(request, 'Estoque atualizado com sucesso!')
            return redirect('produto')
    else:
        form = EstoqueForm(instance=estoque)
        
    return render(request, 'produto/estoque.html', {'form': form, 'produto': produto})

# --- BUSCA GENÉRICA / AUTOCOMPLETE (Atividade 15) ---
def buscar_dados(request, app_model):
    termo = request.GET.get('q', '')
    app_label, model_name = app_model.split('.')
    model = apps.get_model(app_label, model_name)
    resultados = model.objects.filter(nome__icontains=termo)[:10]
    dados = [{'id': obj.id, 'nome': obj.nome} for obj in resultados]
    return JsonResponse(dados, safe=False)

# --- PEDIDOS (Atividades 16 e 17) ---

def pedido(request):
    """Lista todos os pedidos (Slide 6 - Atividade 16)"""
    lista = Pedido.objects.all().order_by('-id')
    return render(request, 'pedido/lista.html', {'lista': lista})

def novo_pedido(request, cliente_id):
    """Cria um novo pedido para um cliente (Atividade 16)"""
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    pedido = Pedido.objects.create(cliente=cliente, status=1) 
    return redirect('detalhes_pedido', id=pedido.id)

def detalhes_pedido(request, id):
    """Exibe detalhes e gerencia inclusão de itens (Atividade 17)"""
    pedido = get_object_or_404(Pedido, pk=id)
    if request.method == 'POST':
        form = ItemPedidoForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.pedido = pedido
            item.save()
            messages.success(request, "Produto adicionado!")
            return redirect('detalhes_pedido', id=id)
    else:
        form = ItemPedidoForm()
        
    return render(request, 'pedido/detalhes.html', {
        'pedido': pedido, 
        'form': form
    })

def remover_item_pedido(request, id):
    """Remove um item específico de um pedido"""
    item = get_object_or_404(ItemPedido, pk=id)
    pedido_id = item.pedido.id
    item.delete()
    messages.success(request, "Produto removido!")
    return redirect('detalhes_pedido', id=pedido_id)