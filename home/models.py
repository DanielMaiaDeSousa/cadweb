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
        if self.preco:
            valor = "{:,.2f}".format(self.preco).replace(",", "X").replace(".", ",").replace("X", ".")
            return f"R$ {valor}"
        return "R$ 0,00"

class Estoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='estoque')
    quantidade = models.IntegerField(default=0)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.produto.nome} - {self.quantidade}"

class Pedido(models.Model):
    STATUS_CHOICES = [
        (1, 'Novo'),
        (2, 'Em Andamento'),
        (3, 'Concluído'),
        (4, 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    produtos = models.ManyToManyField(Produto, through='ItemPedido')
    data_pedido = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)

    @property
    def data_pedidof(self):
        if self.data_pedido:
            return self.data_pedido.strftime('%d/%m/%Y %H:%M')
        return None
    
    @property
    def valor_total_pedido(self):
        """Soma o total de todos os itens associados a este pedido"""
        itens = self.itempedido_set.all()
        return sum(item.total_item for item in itens)

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    qtde = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_item(self):
        """Calcula o valor total deste item (quantidade x preço)"""
        if self.qtde and self.preco:
            return self.qtde * self.preco
        return 0

    def __str__(self):
        return f"{self.produto.nome} (Qtd: {self.qtde})"