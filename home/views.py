from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.apps import apps

# Importação de modelos e formulários corrigida
from .models import Categoria, Cliente, Produto, Estoque, Pedido, ItemPedido, Pagamento
from .forms import CategoriaForm, ClienteForm, ProdutoForm, EstoqueForm, ItemPedidoForm, PagamentoForm

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

# --- ESTOQUE ---
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
# home/views.py

# home/views.py

def buscar_dados(request, app_model):
    termo = request.GET.get('q', '')
    app_label, model_name = app_model.split('.')
    model = apps.get_model(app_label, model_name)
    
    # Filtramos os produtos pelo nome
    resultados = model.objects.filter(nome__icontains=termo)[:10]
    
    dados = []
    for obj in resultados:
        item = {
            'id': obj.id, 
            'nome': obj.nome,
        }
        
        # Se for um Produto, adicionamos o preço e a imagem
        if hasattr(obj, 'preco') and obj.preco:
            item['preco'] = str(obj.preco)
            
        if hasattr(obj, 'img_base64'):
            # O JS espera o campo 'img_base64'
            item['img_base64'] = obj.img_base64 if obj.img_base64 else None
            
        dados.append(item)
        
    return JsonResponse(dados, safe=False)

# --- PEDIDOS ---
def pedido(request):
    lista = Pedido.objects.all().order_by('-id')
    return render(request, 'pedido/lista.html', {'lista': lista})

def novo_pedido(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    pedido_obj = Pedido.objects.create(cliente=cliente, status=1) 
    return redirect('detalhes_pedido', id=pedido_obj.id)

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

def remover_item_pedido(request, id):
    item = get_object_or_404(ItemPedido, pk=id)
    pedido_id = item.pedido.id
    item.delete()
    messages.success(request, "Produto removido!")
    return redirect('detalhes_pedido', id=pedido_id)

def remover_pedido(request, id):
    pedido_obj = get_object_or_404(Pedido, pk=id)
    pedido_obj.delete()
    messages.success(request, "Pedido removido!")
    return redirect('pedido')

# --- PAGAMENTOS ---
def registrar_pagamento(request, pedido_id):
    # Busca o pedido ou retorna 404 caso não exista
    pedido_obj = get_object_or_404(Pedido, pk=pedido_id)
    
    if request.method == 'POST':
        valor = request.POST.get('valor')
        forma = request.POST.get('forma')
        
        if valor and forma:
            try:
                # Converte o valor para decimal tratando a vírgula para o formato Python
                valor_decimal = float(valor.replace(',', '.'))
                
                # INCREMENTO 1: Validação rigorosa para impedir saldo negativo
                if valor_decimal > pedido_obj.debito_restante:
                    messages.error(
                        request, 
                        f"Erro: O valor (R$ {valor_decimal:.2f}) excede o débito restante (R$ {pedido_obj.debito_restante:.2f})."
                    )
                elif valor_decimal <= 0:
                    messages.error(request, "Erro: O valor do pagamento deve ser maior que zero.")
                else:
                    # Cria o registro de pagamento no banco de dados
                    Pagamento.objects.create(
                        pedido=pedido_obj,
                        valor=valor_decimal,
                        forma=forma
                    )
                    
                    # INCREMENTO 2: Atualização automática de status
                    # Se após o pagamento o débito for zerado, o pedido é concluído automaticamente
                    if pedido_obj.debito_restante <= 0:
                        pedido_obj.status = 3  # Status 3 corresponde a 'Concluído'
                        pedido_obj.save()
                        messages.success(request, "Pagamento total recebido. Pedido concluído!")
                    else:
                        messages.success(request, "Pagamento parcial registrado com sucesso!")
                        
            except ValueError:
                messages.error(request, "Erro: O valor digitado é inválido.")
        
        # Redireciona para a mesma página para atualizar o histórico e os totais
        return redirect('registrar_pagamento', pedido_id=pedido_id)

    # Renderiza a página de pagamentos enviando o objeto pedido atualizado
    return render(request, 'pedido/pagamento.html', {'pedido': pedido_obj})