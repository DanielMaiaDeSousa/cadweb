from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ItemPedido, Estoque, Pagamento, Pedido
from decimal import Decimal

@receiver(post_delete, sender=ItemPedido)
def estornar_estoque(sender, instance, **kwargs):
    """Devolve a quantidade ao estoque se um item for removido do pedido."""
    try:
        estoque = Estoque.objects.get(produto=instance.produto)
        estoque.quantidade += instance.qtde
        estoque.save()
    except Estoque.DoesNotExist:
        pass

@receiver(post_save, sender=Pagamento)
def baixar_estoque_ao_pagar(sender, instance, created, **kwargs):
    """Baixa o estoque e finaliza o pedido quando o valor total é pago."""
    pedido = instance.pedido
    
    # Verificação do débito restante usando Decimal
    if pedido.debito_restante <= Decimal('0.00') and pedido.status != 3:
        for item in pedido.itempedido_set.all():
            estoque, _ = Estoque.objects.get_or_create(produto=item.produto)
            estoque.quantidade = max(estoque.quantidade - item.qtde, 0)
            estoque.save()
            
        pedido.status = 3  # Status Concluído
        pedido.save()