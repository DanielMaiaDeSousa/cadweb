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