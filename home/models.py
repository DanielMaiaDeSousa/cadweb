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