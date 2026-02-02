from django.test import TestCase, Client
from django.urls import reverse
from home.forms import PagamentoForm
from home.models import Cliente, Produto, Pedido, ItemPedido, Pagamento
from decimal import Decimal

class PagamentoFormTests(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(nome='Cliente Teste', cpf='000.000.000-00', datanasc='1990-01-01')
        self.produto = Produto.objects.create(nome='Produto 1', preco=Decimal('100.00'), categoria=1)
        self.pedido = Pedido.objects.create(cliente=self.cliente)
        ItemPedido.objects.create(pedido=self.pedido, produto=self.produto, qtde=1, preco=Decimal('100.00'))

    def test_valor_com_virgula_aceito(self):
        form = PagamentoForm(data={
            'valor': '1.234,56',
            'forma': 'dinheiro',
            'tipo': 'a_vista',
            'parcelas': 1,
            'pedido': self.pedido.id
        }, pedido=self.pedido)
        self.assertTrue(form.is_valid())
        pagamento = form.save(commit=False)
        self.assertEqual(pagamento.valor, Decimal('1234.56'))

    def test_valor_maior_que_debito_rejeitado(self):
        # Débito do pedido é 100.00
        form = PagamentoForm(data={
            'valor': '200,00',
            'forma': 'dinheiro',
            'tipo': 'a_vista',
            'parcelas': 1,
            'pedido': self.pedido.id
        }, pedido=self.pedido)
        self.assertFalse(form.is_valid())
        self.assertIn('valor', form.errors)
        self.assertTrue(any('excede o débito restante' in e for e in form.errors['valor']))

    def test_parcelas_invalidas(self):
        form = PagamentoForm(data={
            'valor': '50,00',
            'forma': 'dinheiro',
            'tipo': 'parcelado',
            'parcelas': 0,
            'pedido': self.pedido.id
        }, pedido=self.pedido)
        self.assertFalse(form.is_valid())
        self.assertIn('parcelas', form.errors)

class RegistrarPagamentoViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.cliente = Cliente.objects.create(nome='Cliente Teste 2', cpf='111.111.111-11', datanasc='1990-01-01')
        self.produto = Produto.objects.create(nome='Produto 2', preco=Decimal('50.00'), categoria=1)
        self.pedido = Pedido.objects.create(cliente=self.cliente)
        ItemPedido.objects.create(pedido=self.pedido, produto=self.produto, qtde=2, preco=Decimal('50.00'))

    def test_post_valido_cria_pagamento(self):
        url = reverse('registrar_pagamento', args=[self.pedido.id])
        response = self.client.post(url, data={
            'valor': '50,00',
            'forma': 'dinheiro',
            'tipo': 'a_vista',
            'parcelas': 1,
            'pedido': self.pedido.id
        })
        # Redireciona após sucesso
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Pagamento.objects.filter(pedido=self.pedido).count(), 1)

    def test_post_invalido_reexibe_form_com_erro(self):
        url = reverse('registrar_pagamento', args=[self.pedido.id])
        response = self.client.post(url, data={
            'valor': '1000,00',  # excede o débito
            'forma': 'dinheiro',
            'tipo': 'a_vista',
            'parcelas': 1,
            'pedido': self.pedido.id
        })
        # Deve reexibir a página com erros (status 200)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'excede o débito restante')