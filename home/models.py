from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    ordem = models.IntegerField()

    def __str__(self):
        return self.nome
    
class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=15, verbose_name='C.P.F')
    datanasc = models.DateField(verbose_name='Data de Nascimento')
    
    def __str__(self):
        return self.nome
    
    @property
    def datanasc_formatada(self):
        """Retorna a data de nascimento no formato DD/MM/AAAA."""
        if self.datanasc:
            return self.datanasc.strftime('%d/%m/%Y')
        return ""
        
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) 
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    img_base64 = models.TextField(blank=True)

    def __str__(self):
        return self.nome
    
    @property
    def preco_formatado(self):
        """Formata o preço para R$ sem usar locale (seguro para Vercel)."""
        if self.preco:
            valor = "{:,.2f}".format(self.preco).replace(",", "X").replace(".", ",").replace("X", ".")
            return f"R$ {valor}"
        return "R$ 0,00"
    
# ---- ESTOQUE ----
class Estoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='estoque')
    quantidade = models.IntegerField(default=0)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.produto.nome} - {self.quantidade}"
    
def ajustar_estoque(request, id):
    produto = get_object_or_404(Produto, pk=id)
    estoque, created = Estoque.objects.get_or_create(produto=produto)
    if request.method == 'POST':
        quantidade = request.POST.get('quantidade')
        estoque.quantidade = quantidade
        estoque.save()
        messages.success(request, 'Estoque atualizado!')
        return redirect('produto')
    return render(request, 'produto/estoque.html', {'item': produto, 'estoque': estoque})

# --- PEDIDOS ---
    
# home/models.py
from django.db import models

class Pedido(models.Model):
    # Status possíveis para o pedido [cite: 314]
    STATUS_CHOICES = [
        (1, 'Novo'),
        (2, 'Em Andamento'),
        (3, 'Concluído'),
        (4, 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    # Relacionamento muitos-para-muitos com Produto através de ItemPedido [cite: 314]
    produtos = models.ManyToManyField(Produto, through='ItemPedido')
    data_pedido = models.DateTimeField(auto_now_add=True) # Data automática [cite: 314, 315]
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)

    @property
    def data_pedidof(self):
        """Retorna a data formatada para exibição [cite: 317, 318]"""
        if self.data_pedido:
            return self.data_pedido.strftime('%d/%m/%Y %H:%M')
        return None

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    qtde = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.produto.nome} (Qtd: {self.qtde})"