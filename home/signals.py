# home/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ItemPedido, Estoque, Pagamento

# Não baixamos o estoque ao criar ItemPedido — faremos isso quando o pedido for pago.
@receiver(post_delete, sender=ItemPedido)
def estornar_estoque(sender, instance, **kwargs):
    # Se um item for removido do pedido, devolvemos a quantidade ao estoque
    try:
        estoque = Estoque.objects.get(produto=instance.produto)
        estoque.quantidade += instance.qtde
        estoque.save()
    except Estoque.DoesNotExist:
        pass

@receiver(post_save, sender=Pagamento)
def baixar_estoque_ao_pagar(sender, instance, created, **kwargs):
    pedido = instance.pedido
    # Se o pedido foi totalmente pago e ainda não está marcado como concluído
    if pedido.debito_restante <= 0 and pedido.status != 3:
        for item in pedido.itempedido_set.all():
            estoque, _ = Estoque.objects.get_or_create(produto=item.produto)
            # Evita estoque negativo; ajusta para o mínimo 0
            estoque.quantidade = max(estoque.quantidade - item.qtde, 0)
            estoque.save()
        pedido.status = 3  # Concluído
        pedido.save()