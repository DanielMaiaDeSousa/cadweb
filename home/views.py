from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
import logging
from decimal import Decimal
from .models import Pedido  # ajuste para o nome correto do seu modelo

# Importação de modelos e formulários
from .models import Categoria, Cliente, Produto, Estoque, Pedido, ItemPedido, Pagamento
from .forms import CategoriaForm, ClienteForm, ProdutoForm, EstoqueForm, ItemPedidoForm, PagamentoForm

logger = logging.getLogger(__name__)

# --- INDEX ---
@login_required
def index(request):
    total_vendas = Pagamento.objects.aggregate(Sum('valor'))['valor__sum'] or 0
    novos_pedidos = Pedido.objects.filter(status=1).count()
    total_clientes = Cliente.objects.count()
    total_produtos = Produto.objects.count()

    contexto = {
        'total_vendas': total_vendas,
        'novos_pedidos': novos_pedidos,
        'total_clientes': total_clientes,
        'total_produtos': total_produtos,
    }
    return render(request, 'index.html', contexto)

# --- CATEGORIAS ---
@login_required
def categoria(request):
    contexto = {'lista': Categoria.objects.all().order_by('ordem')}
    return render(request, 'categoria/lista.html', contexto)

@login_required
def form_categoria(request):
    form = CategoriaForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria salva com sucesso!')
            return redirect('categoria')
    return render(request, 'categoria/formulario.html', {'form': form})

@login_required
def editar_categoria(request, id):
    categoria_obj = get_object_or_404(Categoria, pk=id)
    form = CategoriaForm(request.POST or None, instance=categoria_obj)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria atualizada!')
            return redirect('categoria')
    return render(request, 'categoria/formulario.html', {'form': form})

@login_required
def detalhes_categoria(request, id):
    item = get_object_or_404(Categoria, pk=id)
    return render(request, 'categoria/detalhes.html', {'item': item})

@login_required
def remover_categoria(request, id):
    item = get_object_or_404(Categoria, pk=id)
    item.delete()
    messages.success(request, 'Categoria removida!')
    return redirect('categoria')

# --- CLIENTES ---
@login_required
def cliente(request):
    contexto = {'lista': Cliente.objects.all().order_by('-id')}
    return render(request, 'cliente/lista.html', contexto)

@login_required
def form_cliente(request):
    form = ClienteForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente cadastrado com sucesso!')
            return redirect('cliente')
    return render(request, 'cliente/form.html', {'form': form})

@login_required
def editar_cliente(request, id):
    cliente_obj = get_object_or_404(Cliente, pk=id)
    form = ClienteForm(request.POST or None, instance=cliente_obj)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados do cliente atualizados!')
            return redirect('cliente')
    return render(request, 'cliente/form.html', {'form': form})

@login_required
def detalhes_cliente(request, id):
    item = get_object_or_404(Cliente, pk=id)
    return render(request, 'cliente/detalhes.html', {'item': item})

@login_required
def remover_cliente(request, id):
    item = get_object_or_404(Cliente, pk=id)
    item.delete()
    messages.success(request, 'Cliente removido!')
    return redirect('cliente')

# --- PRODUTOS ---
@login_required
def produto(request):
    contexto = {'lista': Produto.objects.all().order_by('-id')}
    return render(request, 'produto/lista.html', contexto)

@login_required
def form_produto(request):
    form = ProdutoForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto salvo com sucesso!')
            return redirect('produto')
    return render(request, 'produto/form.html', {'form': form})

@login_required
def editar_produto(request, id):
    produto_obj = get_object_or_404(Produto, pk=id)
    form = ProdutoForm(request.POST or None, instance=produto_obj)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto atualizado!')
            return redirect('produto')
    return render(request, 'produto/form.html', {'form': form})

@login_required
def detalhes_produto(request, id):
    produto = get_object_or_404(Produto, pk=id)
    return render(request, 'produto/detalhes.html', {'item': produto})

@login_required
def remover_produto(request, id):
    item = get_object_or_404(Produto, pk=id)
    item.delete()
    messages.success(request, 'Produto removido!')
    return redirect('produto')

# --- ESTOQUE ---
@login_required
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

# --- BUSCA GENÉRICA / AUTOCOMPLETE ---
@login_required
def buscar_dados(request, app_model):
    termo = request.GET.get('q', '')
    app_label, model_name = app_model.split('.')
    model = apps.get_model(app_label, model_name)
    resultados = model.objects.filter(nome__icontains=termo)[:10]
    
    dados = []
    for obj in resultados:
        item = {'id': obj.id, 'nome': obj.nome}
        if hasattr(obj, 'preco') and obj.preco:
            item['preco'] = str(obj.preco)
        if hasattr(obj, 'img_base64'):
            item['img_base64'] = obj.img_base64 if obj.img_base64 else None
        dados.append(item)
    return JsonResponse(dados, safe=False)

# --- PEDIDOS ---
@login_required
def pedido(request):
    lista = Pedido.objects.all().order_by('-id')
    return render(request, 'pedido/lista.html', {'lista': lista})

@login_required
def novo_pedido(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    pedido_obj = Pedido.objects.create(cliente=cliente, status=1) 
    return redirect('detalhes_pedido', id=pedido_obj.id)

@login_required
def detalhes_pedido(request, id):
    pedido_obj = get_object_or_404(Pedido, pk=id)
    if request.method == 'POST':
        form = ItemPedidoForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.pedido = pedido_obj
            item.save()
            messages.success(request, "Produto adicionado!")
            return redirect('detalhes_pedido', id=id)
    else:
        form = ItemPedidoForm()
        
    itens = ItemPedido.objects.filter(pedido=pedido_obj)
    return render(request, 'pedido/detalhes.html', {
        'pedido': pedido_obj, 
        'form': form,
        'itens': itens
    })

@login_required
def remover_item_pedido(request, id):
    item = get_object_or_404(ItemPedido, pk=id)
    pedido_id = item.pedido.id
    item.delete()
    messages.success(request, "Produto removido!")
    return redirect('detalhes_pedido', id=pedido_id)

@login_required
def remover_pedido(request, id):
    pedido_obj = get_object_or_404(Pedido, pk=id)
    pedido_obj.delete()
    messages.success(request, "Pedido removido!")
    return redirect('pedido')

# --- PAGAMENTOS ---
@login_required
def registrar_pagamento(request, pedido_id):
    pedido_obj = get_object_or_404(Pedido, pk=pedido_id)
    form = PagamentoForm(pedido=pedido_obj)
    
    if request.method == 'POST':
        data = request.POST.copy()
        
        # Recupera valores de campos hidden caso os originais sumam no POST
        if not data.get('forma'): data['forma'] = request.POST.get('hidden_forma')
        if not data.get('tipo'): data['tipo'] = request.POST.get('hidden_tipo')

        form = PagamentoForm(data, pedido=pedido_obj)
        if form.is_valid():
            pagamento = form.save(commit=False)
            pagamento.pedido = pedido_obj
            pagamento.save()  # Dispara o Signal de baixa de estoque

            # REFRESH: Atualiza o objeto em memória com o status alterado pelo Signal
            pedido_obj.refresh_from_db() 

            if pedido_obj.status == 3:
                messages.success(request, "Pagamento total recebido. Pedido concluído!")
            else:
                messages.success(request, "Pagamento registrado com sucesso!")

            return redirect('registrar_pagamento', pedido_id=pedido_id)
    
    return render(request, 'pedido/pagamento.html', {'pedido': pedido_obj, 'form': form})

@login_required
def editar_pagamento(request, pagamento_id):
    pagamento = get_object_or_404(Pagamento, id=pagamento_id)
    pedido = pagamento.pedido

    if request.method == 'POST':
        data = request.POST.copy()
        if not data.get('forma'): data['forma'] = request.POST.get('hidden_forma')
        if not data.get('tipo'): data['tipo'] = request.POST.get('hidden_tipo')

        form = PagamentoForm(data, instance=pagamento)
        if form.is_valid():
            form.save()
            messages.success(request, "Pagamento atualizado com sucesso!")
            return redirect('registrar_pagamento', pedido_id=pedido.id)
        else:
            # DEBUG: registra o POST recebido e os erros do form para ajudar diagnóstico
            try:
                print('DEBUG editar_pagamento - POST:', dict(request.POST))
                print('DEBUG editar_pagamento - form.errors:', form.errors.as_json())
                logger.debug('editar_pagamento - POST: %s', dict(request.POST))
                logger.debug('editar_pagamento - form.errors: %s', form.errors.as_json())
            except Exception as e:
                logger.exception('Erro ao registrar debug de editar pagamento: %s', e)
    else:
        form = PagamentoForm(instance=pagamento)

    return render(request, 'pedido/editar_pagamento.html', {'form': form, 'pedido': pedido})

def remover_pagamento(request, pagamento_id):
    pagamento = get_object_or_404(Pagamento, id=pagamento_id)
    pedido_id = pagamento.pedido.id
    pagamento.delete()
    messages.success(request, "Pagamento removido!")
    return redirect('registrar_pagamento', pedido_id=pedido_id)

def nota_fiscal(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    itens = ItemPedido.objects.filter(pedido=pedido)
    pagamentos = Pagamento.objects.filter(pedido=pedido)

    contexto = {
        'pedido': pedido,
        'itens': itens,
        'pagamentos': pagamentos,
    }
    return render(request, 'pedido/nota_fiscal.html', contexto) 

@login_required
def registrar_pagamento(request, pedido_id):
    pedido_obj = get_object_or_404(Pedido, pk=pedido_id)
    form = PagamentoForm(pedido=pedido_obj)
    
    if request.method == 'POST':
        data = request.POST.copy()
        # O JS envia 'hidden_forma' e 'hidden_tipo' se os campos principais estiverem readonly
        if not data.get('forma'): data['forma'] = request.POST.get('hidden_forma')
        if not data.get('tipo'): data['tipo'] = request.POST.get('hidden_tipo')

        form = PagamentoForm(data, pedido=pedido_obj)
        if form.is_valid():
            pagamento = form.save(commit=False)
            pagamento.pedido = pedido_obj
            pagamento.save() 

            # REFRESH: Essencial para ver a mudança feita pelo Signal no status do pedido
            pedido_obj.refresh_from_db()

            if pedido_obj.status == 3:
                messages.success(request, "Pagamento total recebido. Pedido concluído!")
            else:
                messages.success(request, "Pagamento registrado com sucesso!")

            return redirect('registrar_pagamento', pedido_id=pedido_id)
    
    return render(request, 'pedido/pagamento.html', {'pedido': pedido_obj, 'form': form})

@login_required
def editar_pagamento(request, pagamento_id):
    pagamento = get_object_or_404(Pagamento, id=pagamento_id)
    pedido = pagamento.pedido
    if request.method == 'POST':
        data = request.POST.copy()
        # Garante que campos ocultos pelo JS sejam preenchidos no POST
        if not data.get('forma'): data['forma'] = request.POST.get('hidden_forma')
        if not data.get('tipo'): data['tipo'] = request.POST.get('hidden_tipo')
        
        form = PagamentoForm(data, instance=pagamento)
        if form.is_valid():
            form.save()
            messages.success(request, "Pagamento atualizado!")
            return redirect('registrar_pagamento', pedido_id=pedido.id)
    else:
        form = PagamentoForm(instance=pagamento)
    return render(request, 'pedido/editar_pagamento.html', {'form': form, 'pedido': pedido})

@login_required
def remover_pagamento(request, pagamento_id):
    pagamento = get_object_or_404(Pagamento, id=pagamento_id)
    pedido_id = pagamento.pedido.id
    pagamento.delete()
    messages.success(request, "Pagamento removido!")
    return redirect('registrar_pagamento', pedido_id=pedido_id)